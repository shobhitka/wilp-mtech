
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <wait.h>
#include <signal.h>

int main(int argc, char *argv[])
{
    int opt, N = 0, M = 0;

    /* parse the command line options to get the port and number of childs to spawn */
    while ((opt = getopt(argc, argv, "n:m:")) != -1) {
        switch(opt) {
            case 'n':
                N = atoi(optarg);
                break;
            case 'm':
                M = atoi(optarg);
                break;
            default:
                fprintf(stdout, "Usage: %s -n num_childs -m num-signal\n", argv[0]);
                exit(-1);
        }
    }

    /* validate the user input */
    if (N == 0 || M == 0) {
        fprintf(stderr, "Invalid parameters\n");
        fprintf(stdout, "Usage: %s -n num_childs -m num-signal\n", argv[0]);
        exit(-1);
    }

    fprintf(stdout, "Starting N: %d childs, waiting for M: %d Signals\n", N, M);
    pid_t pid, pids[N];
    for (int i = 0; i< N; i++) {
        pids[i] = -1;
    }

    for (int i = 0; i < N; i++) {
        pid = fork();
        if (pid < 0) {
            /* ideally should not fail unless ulimits reached */
            fprintf(stderr, "fork() failed: %s\n", strerror(errno));
            exit(-1);
        } else if (pid == 0) {
            int signal_cnt = 0;
            sigset_t signal_set;
            siginfo_t signal_info;

            /* let parent spawn all childs first */
            sleep(3);

            sigemptyset(&signal_set);

            /* child  process */
            pid_t mypid = getpid();
            if (mypid % 2 == 0) {
                while(1) {
                    /* even process, wait for SIGUSR1 */
                    sigaddset(&signal_set, SIGUSR1);
                    sigprocmask(SIG_BLOCK, &signal_set, NULL);
                    sigwaitinfo(&signal_set, &signal_info);

                    /* above will be unblocked only if a SIGUSER1 is received, increase the cnt */
                    signal_cnt++;
                    fprintf(stdout, "SIGUSR1 received: %d <--- %d, cnt: %d\n", mypid, signal_info.si_pid, signal_cnt);
                    if (signal_cnt > M) {
                        /* send SIGTERM + SIGKILL to the last process sending SIGUSR1 */
                        kill(signal_info.si_pid, SIGTERM);
                        fprintf(stdout, "SIGTERM sent: %d ---> %d\n", mypid, signal_info.si_pid);

                        sleep(5);

                        kill(signal_info.si_pid, SIGKILL);
                        fprintf(stdout, "SIGKILL sent: %d ---> %d\n", mypid, signal_info.si_pid);

                        sleep(1); /* allow the signals to be sent */

                        fprintf(stdout, "Terminating Self, pid: %d\n", mypid);
                        break;
                    }
                }
            } else {
                //printf("\n");
                sleep(1);
                /* odd process */
                /* send SIGUSR1 to one of the even process before this process */
                for (int i = 0; i < N; i++) {
                    /* for now find first even and send to that */
                    if (pids[i] > 0 && pids[i] % 2 == 0) {
                        /* even process send SIGUSR1 */
                        kill(pids[i], SIGUSR1);
                        fprintf(stdout, "SIGUSR1 sent: %d ---> %d\n", mypid, pids[i]);
                        break;
                    }
                }

                /* wait for SIGTERM if I am the last sender to make even process signal count = M */
                sigaddset(&signal_set, SIGTERM);
                sigprocmask(SIG_BLOCK, &signal_set, NULL);
                sigwaitinfo(&signal_set, &signal_info);

                /* above will be unblocked only if a SIGTERM is received, increase the cnt */
                signal_cnt++;
                fprintf(stdout, "SIGTERM received: %d <--- %d, cnt: %d\n", mypid, signal_info.si_pid, signal_cnt);
                fprintf(stdout, "Terminating by pid: %d\n", signal_info.si_pid);
                while(1) {
                    sleep(5); // wait forever for SIGKILL to come and kill me
                }
            }

#if 0
            /**
             * Here in each child pids[] will have pid filled for the childs that have been 
             * created before this child
            */
            fprintf(stdout, "------ %d -----\n", getpid());
            for (int j = 0; j < N; j++) {
               // if (pids[j] > 0) {
                    fprintf(stdout, "pid%d: %d\n", j, pids[j]);
                //} else {
                    /* we are filling sequentially, so is < 0 menas after this point no pid */
                //    break;
                //}
            }
            fprintf(stdout, "\n");
            while(1)
                sleep(5);
#endif
            exit(0);
        } else {
            /* parent process*/
            pids[i] = pid;
            fprintf(stdout, "Started child: %d\n", pid);
        }
    }

    for (int i = 0; i < N; i++) {
        wait(NULL);
    }

    return 0;
}

/* localtime example */
#include <stdio.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

int interval = 0;

void sig_handler(int signo)
{
    switch(signo) {
        case SIGINT:
            printf("Terminating\n");
            exit(0);
        case SIGALRM:
            time_t rawtime;
            struct tm * timeinfo;

            time ( &rawtime );
            timeinfo = localtime ( &rawtime );
            printf ( "Current local time and date: %s", asctime (timeinfo) );
            alarm(interval);
            break;
        default:
            printf("Unknown signal: %d\n", signo);
            exit(-1);
    }
}

int main (int argc, char *argv[])
{
    // TBD: Proper error check
    interval = atoi(argv[1]);

    signal(SIGINT, sig_handler);
    signal(SIGALRM, sig_handler);

    alarm(interval);

    while (1) {
        sleep(100);
    }

    return 0;
}
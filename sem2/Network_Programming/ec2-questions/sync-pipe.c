#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <string.h>
#include <sys/wait.h>

int main()
{
    pid_t pid1, pid2, pid3;
    int pipe1[2], pipe2[2], pipe3[2];
    char buff[16];

    pipe(pipe1);
    pipe(pipe2);
    pipe(pipe3);

    pid1 = fork(); // c1
    if (pid1 == 0) {
        // first child, needs to run last
        
        // close all unused pipe FDs as this is last process and no one is waiting on this. 
        close(pipe3[1]);
        close(pipe1[0]); close(pipe1[1]);
        close(pipe2[0]); close(pipe2[1]);

        // block for signal with pipe message from parent, as parent is second last and should signal c1
        read(pipe3[0], buff, 16);

        printf("Executing c1\n");
        
        // done synchronising
        close(pipe3[0]);
        
    } else {
        // parent, needs to run second last just before c1
        if (pid1 < 0) {
            perror("fork");
            exit(-1);
        }

        pid2 = fork(); // c2
        if (pid2 == 0) {
            // second child, needs to run second after c3

            // close the unused pipe FDs and wait for signal from C3
            close(pipe1[1]);
            close(pipe2[0]);
            close(pipe3[0]); close(pipe3[1]);

            read(pipe1[0], buff, 16);
            
            printf("Executing c2\n");

            // signal now to parent
            write(pipe2[1], "p-start", strlen("p-start"));

            // done synchronising
            close(pipe1[0]); close(pipe2[1]);

        } else {

            // parent again to spawn next child

            if (pid2 < 0) {
                perror("fork");
                exit(-1);
            }

            pid3 = fork(); // c3
            if (pid3 == 0) {
                // child 3, needs to execute first, start immidiately
                printf("Executing c3\n");

                close(pipe1[0]);
                close(pipe2[0]); close(pipe2[1]);
                close(pipe3[0]); close(pipe3[1]);

                // signal c2 to execute next
                write(pipe1[1], "c2-start", strlen("c2-start"));

                // done synchronising
                close(pipe1[1]);
            } else {
                if (pid3 < 0) {
                    perror("fork");
                    exit(-1);
                }

                // close unused pipe FDs
                close(pipe1[0]); close(pipe1[1]);
                close(pipe2[1]);
                close(pipe3[0]);

                // wait for signal  from C2 to start executing
                read(pipe2[0], buff, 16);

                printf("Executing p\n");

                // wait for c3 and c2 to finish, would be done anyways
                wait(NULL); wait(NULL);

                // signal c1 to run finally
                write(pipe3[1], "c1-start", strlen("c1-start"));

                // done synchronising
                close(pipe2[0]); close(pipe3[1]);

                wait(NULL); // dont'call if we want parent to terminate after signalling c1, in which case c1 beocomes zombie
            }
        }
    }
}
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>

int main()
{
    int pid;
    int pipefd[2];
    int num1, num2;
    int number;

    int ret = pipe(pipefd);
    if (ret < 0) {
        printf("pipe creation failed: %s\n", strerror(errno));
        exit(-1);
    }

    pid = fork();
    switch(pid) {
        case -1:
            printf("chile process creation failed: %s\n", strerror(errno));
            break;
        case 0:
            // child
            close(pipefd[0]);

            printf("child executing\n");
            number = 5;
            ret = write(pipefd[1], &number, sizeof(number));
            if (ret < 0) {
                printf("Sending number 1 failed: %s\n", strerror(errno));
            } else {
                printf("Bytes written = %d\n", ret);
            }
            
            number = 7;
            ret = write(pipefd[1], &number, sizeof(number));
            if (ret < 0) {
                printf("Sending number 2 failed: %s\n", strerror(errno));
            } else {
                printf("Bytes written = %d\n", ret);
            }
            close(pipefd[1]);
            break;
        default:
            // parent
            close(pipefd[1]);

            printf("Waiting for the numbers from child\n");
            // read for the numbers from child
            read(pipefd[0], &num1, sizeof(num1));
            read(pipefd[0], &num2, sizeof(num2));
            
            close(pipefd[0]);
            printf("Sum: %d + %d = %d\n", num1, num2, num1 + num2);
            wait(NULL);
            break;
    }

    printf("%s terminated\n", pid == 0 ? "Child" : "Parent");
    return 0;
}
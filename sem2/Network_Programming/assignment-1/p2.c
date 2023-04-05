/**
 * Problem Statement - P2
 *
 * Write a concurrent TCP server using I/O Multiplexing (select() system call) that does the
 * following.
 * (a) It takes port no on command-line and waits for incoming connections on that port p.
 * (b) It uses select() to handle concurrency.
 * (c) Whenever it receives a message from a client it sends it to rest of the clients connected to it.
 * (d) Server takes N as command-line-argument and creates N children. These children connect to the
 *     server at port p and send random strings of length 5 at every 2 seconds. Do not use sleep() call
 *     here.
 * (e) After every 20th message server sends "hello" message to all the clients connected to it. Children
 *     simply reply with “hello parent”.
*/
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>
#include <signal.h>
#include <sys/select.h>
#include <stdarg.h>
#include <time.h>
#include <errno.h>

#define MAX_MSG_LEN         16
#define LOOPBACK_IP         "127.0.0.1"
#define CLIENT_PORT_START   10000
#define CHILD_SEND_INTERVAL 2 /* seconds */
#define CHILD_MSG_STR_LEN   5 /* as per the problem */

char TAG[12];

void LOG(char *tag, const char * format, ...)
{
	time_t t;
	va_list args;

    struct tm *tmp;
    char timestamp[128];

    va_start(args, format);

    t = time(NULL);
    tmp = localtime(&t);
    strftime(timestamp, sizeof(timestamp), "%a %b %d %H:%M:%S", tmp);

    fprintf(stdout, "[%s][%s] ", timestamp, tag);
    vfprintf(stdout, format, args);

    va_end(args);
}

/* returns the server socket fd on success, else -1 */
int start_server(int port, int conn_queue)
{
    int srvfd;
    struct sockaddr_in server, client;
    int flag = 1;

    srvfd = socket (AF_INET, SOCK_STREAM, 0);

    bzero(&server, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl (INADDR_ANY);
    server.sin_port = htons (port);

    /* Set socket option to resue addr */
	setsockopt(srvfd, SOL_SOCKET, SO_REUSEPORT, (char *) &flag, sizeof(int));

    if(bind(srvfd, (struct sockaddr *) &server, sizeof (server)) < 0) {
        LOG(TAG, "bind failed: %s\n", strerror(errno));
        return -1;
    }

    listen(srvfd, conn_queue);
    return srvfd;
}

int serverfd;
int my_id;
void generate_random_string(int length, char *str)
{
    /* ascii value for lower case alphabets */
    int lower = 97, upper = 122;
    srand(time(0));
    for (int i = 0; i < length; i++) {
        int num = ((rand() + my_id) % (upper - lower + 1)) + lower;
        str[i] = num;
    }
}

void alarm_handler(int signo)
{
    char data[MAX_MSG_LEN];
    memset(data, 0, MAX_MSG_LEN);
    generate_random_string(CHILD_MSG_STR_LEN, data);
    write(serverfd, data, strlen(data));

    alarm(CHILD_SEND_INTERVAL);
}

void run_child(int id, int srv_port, int cport)
{
    sprintf(TAG, "CHILD-%d", cport);
    my_id = id;

    /* child, try to connect to the server and retry till server is up and running */
    int flag = 1;
    char data[MAX_MSG_LEN];
    struct sockaddr_in server, client;

    bzero(&server, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr (LOOPBACK_IP);
    server.sin_port = htons (srv_port);
    serverfd = socket (AF_INET, SOCK_STREAM, 0);
    if (serverfd < 0) {
        LOG(TAG, "socket() failed: %s\n", strerror(errno));
        exit(-4);
    }

    /* enable reuse port */
    setsockopt(serverfd, SOL_SOCKET, SO_REUSEPORT, (char *) &flag, sizeof(int));

    /* Explicitly assigning port number to client which helps in identifying the clients */
    bzero(&client, sizeof(client));
    client.sin_family = AF_INET;
    client.sin_addr.s_addr = INADDR_ANY;
    client.sin_port = htons(cport);
    client.sin_addr.s_addr = inet_addr (LOOPBACK_IP);

    if (bind(serverfd, (struct sockaddr *) &client, sizeof(client)) < 0) {
        LOG(TAG, "client could not bind to dedicated port, using ephemeral port\n");
    }

    /* keep trying till server is available to accept connections */
    while(1) {
        int ret = connect (serverfd, (struct sockaddr *) &server, sizeof (server));
        if (ret < 0) {
            LOG(TAG, "connect() failed: %s, waiting for server to be ready\n", strerror(errno));
            sleep(1);
            continue;
        } else {
            LOG(TAG, "<--> [SERVER] Connected.\n");
            break; /* server up and we are connected */
        }
    }

    signal(SIGALRM, alarm_handler);
    alarm(CHILD_SEND_INTERVAL);

    /* child messgae loop */
    while (1) {
        sleep (2);
    }

    exit(0);
}

int main(int argc, char *argv[])
{
    int opt, port = 0, childs = 0, srvfd;
    char buff[MAX_MSG_LEN];
    int i, cport;

    strcpy(TAG, "SERVER");
    cport = CLIENT_PORT_START;

    /* parse the command line options to get the port and number of childs to spawn */
    while ((opt = getopt(argc, argv, "p:n:c:")) != -1) {
        switch(opt) {
            case 'p':
                port = atoi(optarg);
                break;
            case 'n':
                childs = atoi(optarg);
                break;
            case 'c':
                cport = atoi(optarg);
                break;
            default:
                fprintf(stdout, "Usage: %s -p port -n num-childs [-c child port start]\n", argv[0]);
                exit(-1);
        }
    }

    /* validate the user input */
    if (port == 0 || childs == 0) {
        fprintf(stderr, "Invalid parameters\n");
        fprintf(stdout, "Usage: %s -p port -n num-childs\n", argv[0]);
        exit(-1);
    }

    LOG(TAG, "Server Configuration: [Port: %d, Num Childs: %d, Child Port Start: %d]\n", port, childs, cport);

    /* initialize the server socket */
    LOG(TAG, "Starting server on port: %d\n", port);
    srvfd = start_server(port, childs);
    if (srvfd < 0) {
        LOG(TAG, "Failed to start server on port: %d\n", port);
        exit(-2);
    }

    /* start the N childs */
    for (i = 0; i < childs; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            LOG(TAG, "fork() failed: %s\n", strerror(errno));
            close(srvfd);
            exit (-3);
        } else if (pid == 0) {
            /* use child number as its id */
            run_child(i + 1, port, cport + i + 1);
        } else {
            /* parent, fork the next child */
            continue;
        }
    }

    LOG(TAG, "spawned all childs\n");

    /* allocate an array for as many client FDs as childs plus 1 for server FD itself */
    int sockets[childs + 1];
    int ports[childs + 1];
    int count = 0;
    for (i = 0; i < childs + 1; i++) {
        sockets[i] = -1;
        ports[i] = -1;
    }

    /* store the server fd at the first index */
    sockets[0] = srvfd;
    ports[0] = port;
    count++;

    fd_set read_fdset;

    /**
     * lets configure the FDSET for accepting incoming connection as well handle all clients 
     * this will be a single loop for concurrent server using selct
    */
    while(1) {
        FD_ZERO(&read_fdset);
        for (i = 0; i < count; i++) {
            if (sockets[i] > 0) { /* not needed as count keeps track of valid index but just being paranoid */
                FD_SET(sockets[i], &read_fdset);
            }
        }

        /**
         * After the loop 'last' holds the index of the last socket fd, which would be the largest fd as well
         * for the process. we can safely use this fd + 1 as nfds in select call
        */
        int ret = select(sockets[i - 1] + 1, &read_fdset, NULL, NULL, NULL);
        if (ret < 0) {
            LOG(TAG, "select() failed: %s\n", strerror(errno));
            continue;
        }

        /* have some fd that are set in fdsdt, check them */
        /* check server FD first fro incoming connection */
        if (FD_ISSET(srvfd, &read_fdset)) {
            socklen_t clilen;
            struct sockaddr_in cliaddr;

            int clifd = accept(srvfd, (struct sockaddr *) &cliaddr, &clilen);
            if (clifd > 0) {
                int chport = ntohs(cliaddr.sin_port);
                LOG(TAG, "<--> [CHILD-%d] connected.\n", chport);
                sockets[count] = clifd;
                ports[count] = chport;
                count++;
            } else {
                LOG(TAG, "accept() failed: %s\n", strerror(errno));
            }

            /* skip checking all other FDs if only one FD was set - server fd */
            if (--ret == 0)
                continue;
        }

        for (i = 1; i < count; i++) {
            /* check all clients */
            if (FD_ISSET(sockets[i], &read_fdset)) {
                memset(buff, 0, MAX_MSG_LEN);
                int ret = read(sockets[i], buff, MAX_MSG_LEN);
                if (ret < 0) {
                    LOG(TAG, "read() failed: %s\n", strerror(errno));
                    continue;
                }

                LOG(TAG, "<-- [CHILD-%d] received message: %s\n", ports[i], buff);

                /* send this message to all connected clients */
                for (int j = 1; j < count; j++) {
                    if (i == j)
                        continue; // don't send to the same client who sent the message

                    ret = write(sockets[j], buff, ret);
                    if (ret < 0) {
                        LOG(TAG, "write() failed: %s\n", strerror(errno));
                        continue;
                    }
                }
            }
        }
    }

    close(srvfd);
    return 0;
}
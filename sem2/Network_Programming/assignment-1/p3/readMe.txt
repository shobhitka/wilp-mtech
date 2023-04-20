Tested on
----------
OS - Ubuntu 20.04
GCC - 9.4.0

Steps to compile and Execute
----------------------------
gcc -o testP3 p3.c

./testP3
Usage: ./testP3 -n num_childs -m num-signal
-n num-childs: Number of children to spawn
-m num-signal: Number of SIGUSR1 signals even child should wait for

example run log
----------------

Network_Programming/assignment-1/p3 on  main [$?⇕] via C v9.4.0-gcc took 16s
❯ ./testP3 -n 40 -m 3

Starting N: 40 childs, waiting for M: 3 Signals
Started child: 3561329
Started child: 3561330
Started child: 3561331
Started child: 3561332
Started child: 3561333
Started child: 3561334
Started child: 3561335
Started child: 3561336
Started child: 3561337
Started child: 3561338
Started child: 3561339
Started child: 3561340
Started child: 3561341
Started child: 3561342
Started child: 3561343
Started child: 3561344
Started child: 3561345
Started child: 3561346
Started child: 3561347
Started child: 3561348
Started child: 3561349
Started child: 3561350
Started child: 3561351
Started child: 3561352
Started child: 3561353
Started child: 3561354
Started child: 3561355
Started child: 3561356
Started child: 3561357
Started child: 3561358
Started child: 3561359
Started child: 3561360
Started child: 3561361
Started child: 3561362
Started child: 3561363
Started child: 3561364
Started child: 3561365
Started child: 3561366
Started child: 3561367
Started child: 3561368
3561331: SIGUSR1 sent to ---> 3561330
3561330: SIGUSR1 received from <--- 3561331, rcv_cnt: 1
3561333: SIGUSR1 sent to ---> 3561332
3561332: SIGUSR1 received from <--- 3561333, rcv_cnt: 1
3561332: SIGUSR1 received from <--- 3561335, rcv_cnt: 2
3561335: SIGUSR1 sent to ---> 3561332
3561337: SIGUSR1 sent to ---> 3561336
3561336: SIGUSR1 received from <--- 3561337, rcv_cnt: 1
3561334: SIGUSR1 received from <--- 3561339, rcv_cnt: 1
3561339: SIGUSR1 sent to ---> 3561334
3561332: SIGUSR1 received from <--- 3561341, rcv_cnt: 3
3561341: SIGUSR1 sent to ---> 3561332
3561336: SIGUSR1 received from <--- 3561343, rcv_cnt: 2
3561343: SIGUSR1 sent to ---> 3561336
3561332: SIGUSR1 received from <--- 3561347, rcv_cnt: 4
3561347: SIGUSR1 sent to ---> 3561332
3561349: SIGUSR1 sent to ---> 3561344
3561344: SIGUSR1 received from <--- 3561349, rcv_cnt: 1
3561342: SIGUSR1 received from <--- 3561351, rcv_cnt: 1
3561351: SIGUSR1 sent to ---> 3561342
3561344: SIGUSR1 received from <--- 3561353, rcv_cnt: 2
3561353: SIGUSR1 sent to ---> 3561344
3561342: SIGUSR1 received from <--- 3561355, rcv_cnt: 2
3561336: SIGUSR1 received from <--- 3561345, rcv_cnt: 3
3561336: SIGUSR1 received from <--- 3561357, rcv_cnt: 4
3561355: SIGUSR1 sent to ---> 3561342
3561345: SIGUSR1 sent to ---> 3561336
3561357: SIGUSR1 sent to ---> 3561336
3561344: SIGUSR1 received from <--- 3561359, rcv_cnt: 3
3561359: SIGUSR1 sent to ---> 3561344
3561361: SIGUSR1 sent to ---> 3561336
3561363: SIGUSR1 sent to ---> 3561360
3561360: SIGUSR1 received from <--- 3561363, rcv_cnt: 1
3561365: SIGUSR1 sent to ---> 3561332
3561367: SIGUSR1 sent to ---> 3561338
3561338: SIGUSR1 received from <--- 3561367, rcv_cnt: 1
3561332: SIGTERM sent to ---> 3561347
3561347: SIGTERM received: <--- 3561332, rcv_cnt: 1
3561347: Terminated by pid 3561332
3561336: SIGTERM sent to ---> 3561357
3561357: SIGTERM received: <--- 3561336, rcv_cnt: 1
3561357: Terminated by pid 3561336
3561332: SIGKILL sent to ---> 3561347
3561336: SIGKILL sent to ---> 3561357
3561332: Terminated Self
3561336: Terminated Self


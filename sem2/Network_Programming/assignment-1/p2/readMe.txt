Github Link
------------
The complete code along with Video demo is also available at github location:

https://github.com/shobhitka/wilp-mtech/tree/main/sem2/Network_Programming/assignment-1

Tested on
----------
OS - Ubuntu 20.04
GCC - 9.4.0

Steps to compile and Execute
----------------------------
gcc -o testP2 p2.c

./testP2.c
Usage: ./testP2 -p port -n num-childs [-c child-port-start]
-p port: Server port to listen on
-n num-childs: NUmber of children to spawn as clients
-c child-port-start: Port number to use per child is child id + this number, default 10000

Understanding the logs
----------------------
Each log is of the format
[timestamp][SERVER] <--> [CHILD-<PORT>] <message>
[timestamp][SERVER] <--- [CHILD-<PORT>] <message>
[timestamp][SERVER] ---> [CHILD-<PORT>] <message>

<--> Indicates connection estanlished
---> Message from server to chile identified by its port using CHILD-<PORT>
<--- Message received by SERVER from CHILD-<PORT>
(cnt)  Indicates the number of messages SERVER has received in total. After every 20 messages server sends "hello"
(*) Indicates the "hello" messages which server sends after 20 random messages from clients. After this the (cnt) is reset to (1)

example run log
----------------
sem2/Network_Programming/assignment-1 on  main [$?] via C v9.4.0-gcc
❯ ./test -p 9000 -n 3
[Thu Apr 20 10:39:53][SERVER] Server Configuration: [Port: 9000, Num Childs: 3, Child Port Start: 10000]
[Thu Apr 20 10:39:53][SERVER] Starting server on port: 9000
[Thu Apr 20 10:39:53][SERVER] spawned all childs
[Thu Apr 20 10:39:53][SERVER] <--> [CHILD-10001] connected.
[Thu Apr 20 10:39:53][SERVER] <--> [CHILD-10002] connected.
[Thu Apr 20 10:39:53][SERVER] <--> [CHILD-10003] connected.
[Thu Apr 20 10:39:55][SERVER] <--- [CHILD-10001] savqe (1)
[Thu Apr 20 10:39:55][SERVER] <--- [CHILD-10002] tbwrf (2)
[Thu Apr 20 10:39:55][SERVER] <--- [CHILD-10003] ucxsg (3)
[Thu Apr 20 10:39:55][SERVER] ---> [CHILD-10002] savqe
[Thu Apr 20 10:39:55][SERVER] ---> [CHILD-10003] savqe
[Thu Apr 20 10:39:55][SERVER] ---> [CHILD-10001] tbwrf
[Thu Apr 20 10:39:55][SERVER] ---> [CHILD-10002] ucxsg
[Thu Apr 20 10:39:55][SERVER] ---> [CHILD-10003] tbwrf
[Thu Apr 20 10:39:55][SERVER] ---> [CHILD-10001] ucxsg
[Thu Apr 20 10:39:57][SERVER] <--- [CHILD-10001] iatfb (4)
[Thu Apr 20 10:39:57][SERVER] <--- [CHILD-10002] jbugc (5)
[Thu Apr 20 10:39:57][SERVER] <--- [CHILD-10003] kcvhd (6)
[Thu Apr 20 10:39:57][SERVER] ---> [CHILD-10003] iatfb
[Thu Apr 20 10:39:57][SERVER] ---> [CHILD-10003] jbugc
[Thu Apr 20 10:39:57][SERVER] ---> [CHILD-10002] iatfb
[Thu Apr 20 10:39:57][SERVER] ---> [CHILD-10002] kcvhd
[Thu Apr 20 10:39:57][SERVER] ---> [CHILD-10001] jbugc
[Thu Apr 20 10:39:57][SERVER] ---> [CHILD-10001] kcvhd
[Thu Apr 20 10:39:59][SERVER] <--- [CHILD-10001] tpvkk (7)
[Thu Apr 20 10:39:59][SERVER] <--- [CHILD-10002] uqwll (8)
[Thu Apr 20 10:39:59][SERVER] ---> [CHILD-10003] tpvkk
[Thu Apr 20 10:39:59][SERVER] ---> [CHILD-10003] uqwll
[Thu Apr 20 10:39:59][SERVER] <--- [CHILD-10003] vrxmm (9)
[Thu Apr 20 10:39:59][SERVER] ---> [CHILD-10002] tpvkk
[Thu Apr 20 10:39:59][SERVER] ---> [CHILD-10001] uqwll
[Thu Apr 20 10:39:59][SERVER] ---> [CHILD-10001] vrxmm
[Thu Apr 20 10:39:59][SERVER] ---> [CHILD-10002] vrxmm
[Thu Apr 20 10:40:01][SERVER] <--- [CHILD-10001] qzaia (10)
[Thu Apr 20 10:40:01][SERVER] <--- [CHILD-10002] rabjb (11)
[Thu Apr 20 10:40:01][SERVER] ---> [CHILD-10003] qzaia
[Thu Apr 20 10:40:01][SERVER] ---> [CHILD-10003] rabjb
[Thu Apr 20 10:40:01][SERVER] <--- [CHILD-10003] sbckc (12)
[Thu Apr 20 10:40:01][SERVER] ---> [CHILD-10002] qzaia
[Thu Apr 20 10:40:01][SERVER] ---> [CHILD-10001] rabjb
[Thu Apr 20 10:40:01][SERVER] ---> [CHILD-10001] sbckc
[Thu Apr 20 10:40:01][SERVER] ---> [CHILD-10002] sbckc
[Thu Apr 20 10:40:03][SERVER] <--- [CHILD-10003] bcpsn (13)
[Thu Apr 20 10:40:03][SERVER] <--- [CHILD-10001] zanql (14)
[Thu Apr 20 10:40:03][SERVER] ---> [CHILD-10001] bcpsn
[Thu Apr 20 10:40:03][SERVER] ---> [CHILD-10002] bcpsn
[Thu Apr 20 10:40:03][SERVER] ---> [CHILD-10002] zanql
[Thu Apr 20 10:40:03][SERVER] <--- [CHILD-10002] aborm (15)
[Thu Apr 20 10:40:03][SERVER] ---> [CHILD-10003] zanql
[Thu Apr 20 10:40:03][SERVER] ---> [CHILD-10001] aborm
[Thu Apr 20 10:40:03][SERVER] ---> [CHILD-10003] aborm
[Thu Apr 20 10:40:05][SERVER] <--- [CHILD-10001] vnnno (16)
[Thu Apr 20 10:40:05][SERVER] <--- [CHILD-10002] wooop (17)
[Thu Apr 20 10:40:05][SERVER] ---> [CHILD-10003] vnnno
[Thu Apr 20 10:40:05][SERVER] ---> [CHILD-10002] vnnno
[Thu Apr 20 10:40:05][SERVER] <--- [CHILD-10003] xpppq (18)
[Thu Apr 20 10:40:05][SERVER] ---> [CHILD-10001] wooop
[Thu Apr 20 10:40:05][SERVER] ---> [CHILD-10003] wooop
[Thu Apr 20 10:40:05][SERVER] ---> [CHILD-10001] xpppq
[Thu Apr 20 10:40:05][SERVER] ---> [CHILD-10002] xpppq
[Thu Apr 20 10:40:07][SERVER] <--- [CHILD-10001] llrct (19)
[Thu Apr 20 10:40:07][SERVER] <--- [CHILD-10002] mmsdu (20)
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10003] llrct
[Thu Apr 20 10:40:07][SERVER] <--- [CHILD-10003] nntev (1)
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10003] mmsdu
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10002] llrct
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10001] mmsdu
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10003] hello (*)
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10001] hello (*)
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10002] hello (*)
[Thu Apr 20 10:40:07][SERVER] <--- [CHILD-10001] hello parent
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10002] nntev
[Thu Apr 20 10:40:07][SERVER] ---> [CHILD-10001] nntev
[Thu Apr 20 10:40:07][SERVER] <--- [CHILD-10002] hello parent
[Thu Apr 20 10:40:07][SERVER] <--- [CHILD-10003] hello parent
[Thu Apr 20 10:40:09][SERVER] <--- [CHILD-10001] lfvks (2)
[Thu Apr 20 10:40:09][SERVER] <--- [CHILD-10002] mgwlt (3)
[Thu Apr 20 10:40:09][SERVER] <--- [CHILD-10003] nhxmu (4)


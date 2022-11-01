# Suzuki–Kasami Algorithm implementation for Mutual Exclusion

## Test Environemnt
1. Code has been tested using Python 3.8.10, but should work on all veriosn 3.x. Please 
    ```diff
    - Do not use Python2. Python2 will not work
    ```
2. The test operating system is Ubuntu Linux 20.04. Should work on Windows and MAC but not tested
3. Main modules used by the code are all in-built python modules. No other external modules are utilized
4. Below is the kist of modules used. All should be ideally available with default python 3 installaton
    ```
    import queue
    import sys
    import threading
    import signal
    import socket
    from time import sleep
    from random import randint
    ```
5. Comminication channel implementation has been done from scratch using Python sockets

## Code organisation
 | Filename | Description | 
 | -------- | ----------- |
 | algo.py | The main Driver code for testing |
 | channel.py | Communication channel implementation |
 | node.py | Main Site node implementation. Implements the complete algorithm |
 | Readme.md | This Redame file |
 | system.cfg | System configuration input file. Discussed in next section |

## System definition
The site configurations are defined in the **system.cfg**. It should define the IDs of all the sites in the system with their IP address and port.

Refer to below as a test sample input
```
# System Configuration defining all sitesin the distributed system
# Site ID, Site IP Address, Site Port
1, 127.0.0.1, 2022
2, 127.0.0.1, 2023
3, 127.0.0.1, 2024
4, 127.0.0.1, 2025
```
The above define 4 sites, S(i) with i = 1..4

```diff
-Site IDs should all be sequential
```

## Basic steps

1. Start all the sites in different terminals using following command
    ```
    python3 algo.py -i <site_id>
    ```
2. If succesfully initialized the application will drop in a command line shell for the site as given below
3. We can type "help" to see what commands are supported
    ```
    ❯ python3 algo.py -i 1
    Parsed system configuration.
    Starting message receiver thread at site id: 1
    Initialized params for channel: (1 -> 2)
    Initialized params for channel: (1 -> 3)
    Initialized params for channel: (1 -> 4)
    Site ready: 1, HAS_TOKEN: True
    (site:1)$ 
    (site:1)$ 
    (site:1)$ help
    help: This help information
    exit: quit the application
    dump: dump all debug info
    enter: enter critical section
    (site:1)$
    ```
4. **Note that Site 1 always starts with the token**
5. We can then do "enter" command to try to enter CS at the site prompt.
5. We can do "enter" on multiple sites one after the other if needed and algorithm will take care of token management
6. When a site enters critical section, it does a random sleep between 5s to 10s and the processing is indicated by increasing number of "." on the terminal
6. All relevant messages and state of RN and Token [LN, Q] will be printed on the console at every state change
7. We can exit the applicatin by "exit" command or by using "CTRL+C"



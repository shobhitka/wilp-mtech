from lib2to3.pgen2 import token
import queue
from random import randint
import sys
import threading
from time import sleep
from token import tok_name
from typing import Tuple
from channel import ChannelMgr

class Token:
    def __init__(self, num_sites):
        self.LN = [ 0 for i in range(num_sites)]
        self.q = queue.Queue()

    def encode(self):
        return str(self.LN)

class Node:
    def __init__(self, sid):
        self.sites = {}
        self.comms = None
        self.sid = sid

        # parse the config file to know about all the sites
        # in the distributed system
        try:
            with open("system.cfg") as input:
                for line in input:
                    if line[0] == '#':
                        # skip comments
                        continue
                    
                    info = line.split(",")
                    self.sites[int(info[0])] = {'ip': str(info[1].strip()), 'port': int(info[2])}

                input.close()
                print("Parsed system configuration.")
                self.RN = [ 0 for i in range(len(self.sites))]
        except IOError:
            sys.exit("System config file could not be found/opened: system.cfg")
        except:
            sys.exit("File parsing error")

    def dump_info(self):
        print("All site info: " + str(self.sites))
        print(f"RN[{self.sid}]: " + str(self.RN))

    def initialize(self):
        try:
            self.comms = ChannelMgr(self.sid, self.sites[self.sid]['ip'], self.sites[self.sid]['port'])

            # start the thread to receive all inbound messages
            self.comms.start_receiver()

            # initialize outbound communication channel with all other sites
            for key in self.sites:
                if key == self.sid:
                    continue

                self.comms.open(key, self.sites[key]['ip'], self.sites[key]['port'])
                print(f"Initialized params for channel: ({self.sid} -> {key})")
            
            # we enable site with id 1 as having token initially
            self.token = Token(len(self.sites))

            if self.sid == 1:
                self.has_token = True
            else:
                self.has_token = False

            print(f"Site ready: {self.sid}, HAS_TOKEN: {self.has_token}")

        except:
            sys.exit("Failed initializing site")

    def cmd_usage(self):
        print("help: This help information")
        print("exit: quit the application")
        print("dump: dump all debug info")
        print("enter: enter critical section")

    def processCmd(self, cmd):
        if cmd == "help":
            self.cmd_usage();
        elif cmd == "exit":
            print("Cleaning up ... ")
            self.comms.stop_receiver()
            sys.exit("Exiting")
        elif cmd == "dump":
            self.dump_info()
        elif cmd == "enter":
            self.enter_cs()

    def start(self):
        while 1:
            cmd = input(f"(site:{self.sid})$ ")

            # Process commands
            self.processCmd(cmd)

    # critical section execution
    def cs_function(self):
        print("Executing critical section")

        sleep(randint(5,15))

        print("Exitting the critical section")

        # update the last processed request
        self.token.LN[self.sid] = self.RN[self.sid]

        for key in self.sites:
            if key == self.sid:
                continue

            # check if any outstanding request is there
            if key not in self.token.q.queue:
                if self.RN[key - 1] == self.token.LN[key - 1] + 1:
                    self.token.q.put(key)

        print("LN: " + str(self.token.LN))
        print(" Q: " + str(list(self.token.q.queue)))
        if not self.token.q.empty():
            next = self.token.q.get()
            msg = ["TOKEN", self.token.encode()]
            print("TOKEN, " + str(self.sid) + " --> " + str(key))
            self.comms.send(next, msg)

    def enter_cs(self):
        if self.has_token == True:
            print(f"HAS_TOKEN: {self.has_token}: Entering CS")
            self.in_cs = True
            # site has the token and can enter critical section
            # start a thread to execute CS; simulated with random sleep
            th = threading.Thread(target = self.cs_function)
            th.start()
            th.join()
        else:
            # increament local SN
            self.RN[self.sid - 1] += 1
            print("RN = " + str(self.RN))

            # broadcast REQUEST message
            msg = ["REQUEST", self.sid, self.RN[self.sid - 1]]
            for key in self.sites:
                if key == self.sid:
                    continue
                else:
                    print("REQUEST, " + str(self.sid) + " --> " + str(key) + ", SN: " + str(self.RN[self.sid]))
                    self.comms.send(key, str(msg))

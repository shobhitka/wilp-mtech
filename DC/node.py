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
        return ','.join(str(item) for item in self.LN) + ":" + ",".join(str(item) for item in (list(self.q.queue))) + ":"

    def decode(self, data):
        ln_list = data[2].split(",")
        self.LN = [ int(item) for item in ln_list ]

        q_list = data[3].split(",")
        self.q = queue.Queue()
        for item in q_list:
            if item == '':
                break
            self.q.put(item)

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
        #print("All site info: " + str(self.sites))
        print(f"RN: " + str(self.RN))

        if self.has_token:
            print(f"HAS_TOKEN: {self.has_token}")
            print("LN: " + str(self.token.LN))
            print(" Q: " + str(list(self.token.q.queue)))

    def initialize(self):
        try:
            self.comms = ChannelMgr(self.sid, self.sites[self.sid]['ip'], self.sites[self.sid]['port'], self)

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
            self.requested_token = False

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
        self.token.LN[self.sid - 1] = self.RN[self.sid - 1]

        for key in self.sites:
            if key == self.sid:
                continue

            # check if any outstanding request is there
            if key not in self.token.q.queue:
                if self.RN[key - 1] == self.token.LN[key - 1] + 1:
                    self.token.q.put(key)

        if not self.token.q.empty():
            next = self.token.q.get()
            msg = "TOKEN:" + str(self.sid) + ":" + self.token.encode()
            print(f"[SEND][TOKEN] " + str(self.sid) + " --> " + str(key))
            self.comms.send(next, msg)
            self.has_token = False

        self.dump_info()

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
            self.dump_info()

            # broadcast REQUEST message
            msg = "REQUEST:" +  str(self.sid) + ":" + str(self.RN[self.sid - 1])
            for key in self.sites:
                if key == self.sid:
                    continue
                else:
                    print("[SEND][REQUEST] " + str(self.sid) + " --> " + str(key) + ", SN: " + str(self.RN[self.sid]))
                    self.comms.send(key, str(msg))
                    self.requested_token = True

    def callback(self, msg):
        cmd = msg.split(":")

        if cmd[0] == "REQUEST":
            # Token request message received
            site = int(cmd[1])
            sn = int(cmd[2])
            self.RN[site - 1] = max(self.RN[site - 1], sn)
            print(f"[RECV][REQUEST] Msg from site: {site}, SN: {sn}")

            if self.has_token == True and self.RN[site - 1] == self.token.LN[site - 1] + 1:
                msg = "TOKEN:" + str(self.sid) + ":" + self.token.encode()
                print(f"[SEND][TOKEN] " + str(self.sid) + " --> " + str(site))
                self.comms.send(site, str(msg))
                self.has_token = False

            self.dump_info()
        elif cmd[0] == "TOKEN":
            if self.requested_token == False:
                print("TOKEN received in error ?")
                return

            print(f"[RECV][TOKEN] Msg from site: {cmd[1]}")

            # received token, update local token instance
            self.token.decode(cmd)
            self.has_token = True

            if self.requested_token == True:
                self.enter_cs()

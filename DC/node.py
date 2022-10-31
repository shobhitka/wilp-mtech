from queue import Queue
import sys
from channel import ChannelMgr

class Token:
    def __init__(self, num_sites):
        self.LN = [ 0 for i in range(num_sites)]
        self.q = Queue()

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
            
            if self.sid == 1:
                # we enable site with id 1 as having token initially
                self.token = Token(len(self.sites))
                self.has_token = True

            print(f"Site ready: {self.sid}, HAS_TOKEN: {self.has_token}")

        except:
            sys.exit("Failed initializing site")

    def cmd_usage(self):
        print("help: This help information")
        print("exit: quit the application")
        print("dump: dump all debug info")

    def processCmd(self, cmd):
        if cmd == "help":
            self.cmd_usage();
        elif cmd == "exit":
            print("Cleaning up ... ")
            self.comms.stop_receiver()
            sys.exit("Exiting")
        elif cmd == "dump":
            self.dump_info()

    def start(self):
        while 1:
            cmd = input(f"(site:{self.sid})$ ")

            # Process commands
            self.processCmd(cmd)
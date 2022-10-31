from re import A
import sys
from channel import ChannelMgr

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
        except IOError:
            sys.exit("System config file could not be found/opened: system.cfg")
        except:
            sys.exit("File parsing error")

    def dump_info(self):
        print(str(self.sites))

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
            
            print(f"Site ready: {self.sid}")
        except:
            sys.exit("Failed initializing site")

    def cmd_usage(self):
        print("help: This help information")
        print("exit: quit the application")

    def processCmd(self, cmd):
        if cmd == "help":
            self.cmd_usage();
        elif cmd == "exit":
            print("Cleaning up ... ")
            self.comms.stop_receiver()
            sys.exit("Exiting")

    def start(self):
        while 1:
            cmd = input(f"(site:{self.sid})$ ")

            # Process commands
            self.processCmd(cmd)
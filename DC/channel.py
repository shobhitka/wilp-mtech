import socket
import sys
import threading
from time import sleep

class ChannelThread(threading.Thread):

    def __init__(self, chmgr):
        self.chmgr = chmgr
        threading.Thread.__init__(self)

    def run(self):
        print(f"Starting message receiver thread at site id: {self.chmgr.getsite()}")
        while 1:
            try:
                # receive message and dump them for now
                bytes, address = self.chmgr.receive_messages()
                print("Msg: " + bytes.decode() + ", from: " + str(address))
            except:
                print("Receiver channel thread terminated. Exiting")
                sys.exit(1)

class ChannelMgr:

    MAX_BUFF_SIZE = 64

    def __init__(self, sid, sip, sport):
        self.sid = sid
        self.sip = sip
        self.sport = sport
        self.chthread = None
        self.channels = {}
        self.cnt = 0

        try:
            # Create the receive channel socket
            self.skt = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

            # bind it to local port
            self.skt.bind((sip, sport))

            # create a receiver thread for messages
            self.chthread = ChannelThread(self)
        except:
            print("Creating communication channel receiver thread failed")
            sys.exit()

    def start_receiver(self):
        self.chthread.start()

    def open(self, did, dip, dport):
        daddr = (dip, dport)
        self.channels[did] =daddr
        self.cnt += 1

        # return the site ID itself as the channel id
        return did

    def receive_messages(self):
        return self.skt.recvfrom(self.MAX_BUFF_SIZE)

    def send(self, did, message):
        try:
            self.skt.sendto(str.encode(message), self.channels[did])
            return 0
        except:
            print(f"Sending message failed to site id: {did}\n")
            return -1

    def getsite(self):
        return self.sid

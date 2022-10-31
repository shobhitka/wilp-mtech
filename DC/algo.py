from time import sleep
import channel

import sys, getopt

def usage():
    print("python algo.py -i <site_id>")
    sys.exit(0)

def main (argv):
    site_id = None
    site_port = None
    dest_id = None
    dest_port = None
    try:
        opts, args = getopt.getopt(argv, "hs:p:d:i:")
    except:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt == '-s':
            site_id = int(arg)
        elif opt == "-p":
            site_port = int(arg)
        elif opt == '-d':
            dest_id = int(arg)
        elif opt == "-i":
            dest_port = int(arg)
        else:
            usage()

    if site_id is None or site_port is None or dest_id is None or dest_port is None:
        usage()

    print(f"Site id: {site_id}")
    print(f"Site port: {site_port}")
    print(f"Dest Site id: {dest_id}")
    print(f"Dest Site port: {dest_port}")

    # Driver to test
    comms = channel.ChannelMgr(site_id, "127.0.0.1", site_port)
    comms.start_receiver()
    comms.open(dest_id, "127.0.0.1", dest_port)
    sleep(5.0)
    comms.send(dest_id, f"Hello from site: {site_id}")

if __name__ == "__main__":
    main(sys.argv[1:])

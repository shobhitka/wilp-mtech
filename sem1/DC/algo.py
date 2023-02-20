from time import sleep
import channel
import sys, getopt
from node import Node

def usage():
    print("python algo.py -i <site_id>")
    sys.exit(0)

def main (argv):
    site_id = None
    try:
        opts, args = getopt.getopt(argv, "hi:")
    except:
        usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt == "-i":
            site_id = int(arg)
        else:
            usage()

    if site_id is None:
        usage()

    # Driver to test
    localsite = Node(site_id)
    localsite.initialize()
    localsite.start()

if __name__ == "__main__":
    main(sys.argv[1:])

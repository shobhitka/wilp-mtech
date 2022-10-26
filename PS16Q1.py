import sys

# define operations on the ticketing system
INIT_TICKET_SYSTEM  = 'ticketSystem'
ADD_PERSON          = 'addPerson'
GET_WINDOW          = 'getWindow'
IS_OPEN             = 'isOpen'
GIVE_TICKET         = 'giveTicket'

# Define errors
ERR_SUCCESS         = 0
ERR_MISSING_PARAMS  = -1
ERR_INVALID_PARAMS  = -2
ERR_INVALID_INPUT   = -3

class Logger(object):
    def __init__ (self, file = "outputPS16Q1.txt"):
        self.log = open(file, "w")

    def write (self, message, prefix = ""):
        if prefix:
            data = prefix + ": " + message + "\n"
        else:
            data = message + "\n"

        self.log.write(data + "\n")

        # For now dump on stdout too, commented for final code
        # only log in specififed files
        # print(data)

# prompt logger
logp = Logger("promptsPS16Q1.txt")

# output logger
logo = Logger("outputPS16Q1.txt")

# Queue ADT implementation. Use explicitely a count variable 'cnt'
# 'cnt' directly tracks the queue size, with this we do not waste
# one slot to distinguish between full and empty when 'front' == 'rear'
class Queue:
    def __init__(self, win, n):
        self.size = n
        self.item = [ None for i in range(n) ]
        self.cnt = 0
        self.front = 0
        self.rear = 0
        self.win = win

    def isEmpty(self):
        if self.cnt == 0:
            return True
        else:
            return False

    def getSize(self):
        return self.cnt

    def enqueue(self, pid):
        if self.cnt == self.size:
            logp.write("Enqueue failed: Queue full for window id - " + str(self.win + 1))
            return -1

        self.item[self.rear] = pid
        self.rear = (self.rear + 1) % self.size
        self.cnt = self.cnt + 1
        return 0

    def dequeue(self):
        if self.isEmpty():
            logp.write("Dequeue failed: Queue empty for window id - " + str(self.win + 1))
            return -1

        item = self.item[self.front]
        self.item[self.front] = None
        self.front = (self.front + 1) % self.size
        self.cnt = self.cnt - 1
        return item

    def getFront(self):
        if self.isEmpty():
            return -1

        return self.item[self.front]

    # method to get the queue list of filled slots
    # loop though all slots. Worst case queue is full
    # and this routine will run in O(n) time
    def getQueueElems(self):
        if self.isEmpty():
            return []

        i = self.front
        q = []
        while True:
            q = q + [self.item[i]]
            i = (i + 1) % self.size
            if i == self.rear:
                break
        return q

class BoxOffice:
    def __init__(self, w, n):
        # queue size
        self.n = n

        # number of windows
        self.w = w

        # Initialize as many queues as the number of windows
        self.queues = [ Queue(j, n) for j in range(w) ]

        # Initialise all windows as closed except 1st window
        self.windows = [ False for i in range(w) ]
        self.windows[0] = True

    def isOpen(self, win):
        index = win - 1
        if 0 <= index < self.w:
            return self.windows[index];
        else:
            logp.write("Invalid window id given: " + str(win))
            return False

    def getWindow(self, win):
        # use window index
        index = win - 1
        if 0 <= index < self.w:
            return self.queues[win - 1].getQueueElems()
        else:
            logp.write("Invalid window id given: " + str(win))
            return []

    def addPerson(self, personId):
        window = -1
        to_open = -1
        cnt = self.n
        for i in range (self.w):
            # loop through all open windows and choose the one with
            # smallest queue size
            # This will also make sure if two windows are having same 
            # size, the one with smalles index(window ID) will be used
            # worst case this will loop through all windows and find
            # them all open and full. Will run in O(w) time
            if (self.windows[i] is True):
                if self.queues[i].getSize() < cnt:
                    cnt =  self.queues[i].getSize()
                    window = i
            elif to_open == -1:
                # in the same parsing also store the next closed window 
                # that can be opened in case no open windoes have space
                to_open = i

        if window == -1 and to_open == -1:
            # All windows are open and none has any free space
            return -1

        if window != -1:
            # found a open window with smallest queue
            self.queues[window].enqueue(personId)
            return window + 1 # Window absolute ID
        else:
            # Open a new window and enqueue to that window
            self.windows[to_open] = True
            self.queues[to_open].enqueue(personId)
            return to_open + 1

    def giveTicket(self):
        cnt = 0
        # This has to loop through the window list
        # Worst case all windows might be open and we have to
        # giveTicket at all of them. So this will run in O(w)
        # time
        for i in range(self.w):
            # window closed
            if self.windows[i] == False:
                continue

            # Window open but empty
            if self.queues[i].getSize() == 0:
                continue

            # give ticket at this window
            self.queues[i].dequeue()
            cnt = cnt + 1

        return cnt

# Validate parameters and return a list of params for the command
# after validation and converting to int
def validateParams(cmd):
    try:
        if cmd[0] == INIT_TICKET_SYSTEM:
            # expects two params as integers
            if len(cmd) != 3:
                logp.write("Missing or extra parameters", INIT_TICKET_SYSTEM)
                return [ERR_MISSING_PARAMS]

            # try to typecase parameters to int to validate them for integers 
            # if wrong params, it will cause excepition
            return [int(cmd[1]), int(cmd[2])]

        elif cmd[0] == GIVE_TICKET:
            # No parameters are expected, ignore if any given
            return [ERR_SUCCESS]
        else:
            # All remaining commands only take 1 integer parameter as input
            if len(cmd) != 2:
                logp.write("Missing or extra parameters", INIT_TICKET_SYSTEM)
                return [ERR_MISSING_PARAMS]

            return [int(cmd[1])]
    except:
        logp.write("Invalid parameters", cmd[0])
        return [ERR_INVALID_PARAMS]

def processInput(line):
    if line == "\n":
        # skip empty input line
        return ERR_SUCCESS

    # declare global BoxOffice object
    global bo
    cmd = line.strip().split(":")

    try:
        # quick check if this is initialized or not
        # should be initialized for all commands except
        # INIT_TICKET_SYSTEM
        bo
    except:
        # if command is not init and bo is not initialized then
        # init command was not sent before issuing other commands
        if cmd[0] != INIT_TICKET_SYSTEM:
            logp.write("Invalid input", cmd[0])
            return ERR_INVALID_INPUT

    # Further validation of each command and its parameters
    params = validateParams(cmd)

    if params[0] < 0:
        # Validation failed
        return params[0]

    if cmd[0] == INIT_TICKET_SYSTEM:
        bo = BoxOffice(params[0], params[1])
    elif cmd[0] == ADD_PERSON:
        retVal = bo.addPerson(params[0])
        if retVal < 0:
            logo.write(line.strip() + " >> all queues are full")
        else:
            logo.write(line.strip() + " >> " + str(retVal))
    elif cmd[0] == GET_WINDOW:
        retVal = bo.getWindow(params[0])
        logo.write(line.strip() + " >> " + str(retVal))
    elif cmd[0] == IS_OPEN:
        if params[0] < 1 or params[0] > bo.w:
            return ERR_INVALID_INPUT
        else:
            if bo.isOpen(params[0]):
                logo.write(line.strip() + " >> TRUE")
            else:
                logo.write(line.strip() + " >> FALSE")

    elif cmd[0] == GIVE_TICKET:
        retVal = bo.giveTicket()
        logo.write(line.strip() + " >> " + str(retVal))
    else:
        print("Unsupported command")

    return ERR_SUCCESS

def main():
    try:
        with open("inputPS16Q1.txt") as input:
            for line in input:
                retVal = processInput(line)
                if retVal < 0:
                    logp.write("Invalid input. Exiting")
                    break

            input.close()
    except IOError:
        sys.exit("File could not be found/opened: inputPS16Q1.txt")
    except:
        sys.exit("Internal error")

if __name__ == "__main__":
    main()
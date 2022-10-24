from asyncio import queues
from asyncore import write
from textwrap import wrap


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
    def __init__ (self, file = "promptsPS16Q1.txt"):
        self.log = open(file, "w")

    def write (self, message, prefix = ""):
        if prefix:
            data = prefix + ": " + message + "\n"
        else:
            data = message + "\n"

        self.log.write(data)

        # For now dump on stdout too
        print(data)

# prompt logger
logp = Logger("promptsPS16Q1.txt")

# output logger
logo = Logger("outputPS16Q1.txt")

class Queue:
    def __init__(self, n):
        self.size = n
        self.item = [ None for i in range(n) ]
        self.cnt = 0
        self.front = 0
        self.rear = 0

    def isEmpty(self):
        if self.cnt == 0:
            return True
        else:
            return False

    def getSize(self):
        return self.cnt

    def enqueu(self, pid):
        if self.cnt == self.size:
            return -1

        self.item[self.rear] = pid
        self.rear = (self.rear + 1) % self.size
        self.cnt = self.cnt + 1
        return 0

    def dequeue(self):
        if self.isEmpty():
            return -1

        self.item[self.front] = None
        self.front = (self.front + 1) % self.size
        return 0

    def getFront(self):
        if self.isEmpty():
            return -1

        return self.item[self.front]

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
    def __init__(self, n, w):
        self.n = n
        self.w = w

        # Initialize as many quesus as the number of windows
        self.queues = [ Queue(n) for j in range(w) ]

        # Initialise all windows as closed except 1st window
        self.windows = [ False for i in range(w) ]
        self.windows[0] = True

    def isOpen(self, win):
        index = win - 1
        if 0 <= index < self.w:
            return self.windows[index];
        else:
            return False

    def getWindow(self, win):
        # use window index
        return self.queues[win - 1].getQueueElems()

    def addPerson(self, personId):
        window = -1
        cnt = self.n
        to_open = -1
        for i in range (self.w):
            # loop through all open windows and choose the one with
            # smallest queue size
            # This will also make sure if two windows are having same 
            # size, the one first checked will be used
            if (self.windows[i] is True):
                if self.queues[i].getSize() < cnt:
                    cnt =  self.queues[i].getSize()
                    window = i
            elif to_open == -1:
                # in the same parsing also store the next closed window 
                # that can be opened in case no open windoes have space
                to_open = i

        if window == -1 and to_open == -1:
            # All windows are open and non ehas any free space
            return -1

        if window != -1:
            self.queues[window].enqueu(personId)
            return window + 1 # Window absolute ID
        else:
            self.windows[to_open] = True
            self.queues[to_open].enqueu(personId)
            return to_open + 1

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
    global bo
    cmd = line.strip().split(":")

    try:
        bo
    except:
        # if command is not init and bo is not initialized then
        # init command was not sent before issuing other commands
        if cmd[0] != INIT_TICKET_SYSTEM:
            logp.write("Invalid input", cmd[0])
            return ERR_INVALID_INPUT

    params = validateParams(cmd)

    if params[0] < 0:
        # Validation failed
        return params[0]

    if cmd[0] == INIT_TICKET_SYSTEM:
        bo = BoxOffice(params[0], params[1])
    elif cmd[0] == ADD_PERSON:
        retVal = bo.addPerson(params[0])
        if retVal < 0:
            logo.write(line + " >> all queues are full")
        else:
            logo.write(line.strip() + " >> " + str(retVal))
    elif cmd[0] == GET_WINDOW:
        retVal = bo.getWindow(params[0])
        logo.write(line.strip() + " >> " + str(retVal))
    elif cmd[0] == IS_OPEN:
        if params[0] < 0 or params[0] > bo.w:
            return ERR_INVALID_INPUT
        else:
            if bo.isOpen(params[0]):
                logo.write(line.strip() + " >> TRUE")
            else:
                logo.write(line.strip() + " >> FALSE")

    elif cmd[0] == GIVE_TICKET:
        print(GIVE_TICKET)
    else:
        print("Unsupported command")

    return ERR_SUCCESS

def main():
    with open("inputPS16Q1.txt") as input:
        for line in input:
            retVal = processInput(line)
            if retVal < 0:
                logp.write("Invalid input. Exiting")
                break

        input.close()

if __name__ == "__main__":
    main()
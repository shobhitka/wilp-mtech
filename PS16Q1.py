INIT_TICKET_SYSTEM  = 'ticketSystem'
ADD_PERSON          = 'addPerson'
GET_WINDOW          = 'getWindow'
IS_OPEN             = 'isOpen'
GIVE_TICKET         = 'giveTicket'

# Define errors
ERR_SUCCESS         = 0
ERR_MISSING_PARAMS  = -1
ERR_INVALID_PARAMS  = -2

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

logp = Logger("promptsPS16Q1.txt")
logo = Logger("outputPS16Q1.txt")

class BoxOffice:
    def __init__(self, n, w) -> None:
        pass

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
    cmd = line.strip().split(":")
    params = validateParams(cmd)

    if params[0] < 0:
        # Validation failed
        return params[0]

    if cmd[0] == INIT_TICKET_SYSTEM:
        bo = BoxOffice(params[0], params[1])

    elif cmd[0] == ADD_PERSON:
        print(ADD_PERSON)
    elif cmd[0] == GET_WINDOW:
        print(GET_WINDOW)
    elif cmd[0] == IS_OPEN:
        print(IS_OPEN)
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
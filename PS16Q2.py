# Define errors
ERR_SUCCESS         = 0
ERR_MISSING_PARAMS  = -1
ERR_INVALID_PARAMS  = -2
ERR_INVALID_INPUT   = -3

class Logger(object):
    def __init__ (self, file = "outputPS16Q2.txt"):
        self.log = open(file, "w")

    def write (self, message, prefix = ""):
        if prefix:
            data = prefix + ": " + message + "\n"
        else:
            data = message + "\n"

        self.log.write(data + "\n")

        # For now dump on stdout too
        print(data)

# prompt logger
logp = Logger("promptsPS16Q2.txt")

# output logger
logo = Logger("outputPS16Q2.txt")

def main():
    with open("inputPS16Q2.txt") as input:
        for line in input:
            logp.write(line.strip())
            
        input.close()

if __name__ == "__main__":
    main()
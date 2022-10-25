# Define errors
ERR_SUCCESS         = 0
ERR_INVALID_INPUT   = -1
ERR_INVALID_FILE    = -2

# Define inputs
FOOD_ITEM_CNT       = "Food Items"
KNAPSACK_MAX_WT     = "Maximum Bag Weight"

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

def max_heapify(arr, n , i):
    root = i
    left = 2 * root
    right = 2 * root + 1
    max = root

    if left < n and arr[left] > arr[root]:
        max = left

    if right < n and arr[max] < arr[right]:
        max = right
    
    # swap the root with max element unless root is really max
    if i != max:
        tmp = arr[i]
        arr[i] = arr[max]
        arr[max] = tmp

        # heapify again with max as the root
        max_heapify(arr, n, max)

# sorted array is stored in arr in increasing order. index 0 is unused
def heapSort(arr, n):
    # start with the rightmost node's parent and loop till index 1
    # index 0 is unused to enable root = i, left = 2i and right = 2i + 1
    for i in range(int(n/2), 0, -1):
        max_heapify(arr, n, i)

    # now swap the root which will be max with last element
    # and reheapify after removing the last element from the
    # array size. Again loop till index 1 as index 0 is unused
    for i in range (n - 1, 0, -1):
        max = arr[1]
        arr[1] = arr[i]
        arr[i] = max

        max_heapify(arr, i, 1)

def parseInputFile(file):
    global item_list
    item_list = []
    global item_cnt
    global max_weight
    try:
        with open(file) as input:
            try:
                for line in input:
                    if line.find(FOOD_ITEM_CNT) != -1:
                        item_cnt = int(line.split(":")[1])
                    elif line.find(KNAPSACK_MAX_WT) != -1:
                        max_weight = int(line.split(":")[1])
                    else: # Food item details
                        item = line.strip().split("/")
                        item_list = item_list + [item[0].strip(), int(item[1]), int(item[2])]
            except:
                logp.write("Invalid input")
                input.close()
                return ERR_INVALID_INPUT
            
            input.close()
    except:
        logp.write("Invalid input file")
        return ERR_INVALID_FILE

def main():
    parseInputFile("inputPS16Q2.txt")
    print("Item Cnt: " + str(item_cnt))
    print("Max weight: " + str(max_weight))
    print("Items: " + str(item_list))

if __name__ == "__main__":
    main()
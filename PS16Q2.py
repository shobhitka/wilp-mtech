import sys

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

    if left < n and arr[left][1] > arr[root][1]:
        max = left

    if right < n and arr[max][1] < arr[right][1]:
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
                        item_list += [[ item[0].strip(), int(item[1]), int(item[2]) ]]
            except:
                input.close()
                return ERR_INVALID_INPUT
            
            input.close()
    except:
        return ERR_INVALID_FILE

def main():
    global calorie_to_weight

    # first slot will be unused as we will create a max heap in this array
    # just initialize to some sane value
    calorie_to_weight = [[ -1, 0.0 ]]

    retval = parseInputFile("inputPS16Q2.txt")
    if retval == ERR_INVALID_FILE:
        sys.exit("File could not be found/opened: inputPS16Q2.txt")
    elif retval == ERR_INVALID_INPUT:
        sys.exit("Invalid input data")

    logp.write("Item Cnt: " + str(item_cnt))
    logp.write("Max weight: " + str(max_weight))
    logp.write("Items: " + str(item_list))

    for i in range(1, item_cnt + 1, 1):
        ratio = round((item_list[i - 1][2] / item_list[i - 1][1]), 2)

        # store the calorie to weight ratio along with the item_list index for the item
        calorie_to_weight += [[ i - 1, ratio ]]

    logp.write("Unsorted calorie_to_weight ratio: " + str(calorie_to_weight))

    # sort the array so that we start picking the items with largest
    # calorie to weight ratio - greedy algorithm
    heapSort(calorie_to_weight, len(calorie_to_weight))

    logp.write("Sorted calorie_to_weight ratio: " + str(calorie_to_weight))

    # Now we simply need to prepare the knapsack contents
    output = [ 0 for i in range(item_cnt) ]
    target_wt = max_weight
    calories = 0
    for i in range(item_cnt, 0, -1):
        index = calorie_to_weight[i][0]
        if item_list[index][1] > target_wt:
            break;
        output[index] = 1
        target_wt -= item_list[index][1]
        calories += item_list[index][2] * item_list[index][1]

    if i > 0: # some items not yet covered
        index = calorie_to_weight[i][0]
        output[index] = target_wt / item_list[index][1]
        calories += (output[index] * item_list[index][2] * item_list[index][1])

    logo.write("Total Calories: " + str(calories))
    logo.write("Food Item selection Ratio:")

    for i in range(item_cnt):
        logo.write(item_list[i][0] + ": " + str(output[i]))

if __name__ == "__main__":
    main()
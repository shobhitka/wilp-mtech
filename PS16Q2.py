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

def main():
    arr = [0, 12, 9, 11, 13, 15, 5, 6, 7]
    with open("inputPS16Q2.txt") as input:
        for line in input:
            logp.write(line.strip())
            
        input.close()

    heapSort(arr, len(arr))

    print(str(arr))

if __name__ == "__main__":
    main()
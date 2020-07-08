import time


if __name__ == "__main__":
    for i in range(2**30 + 1):
        print("decimal: {0:<11d} binary: {0:<32b} hex: {0:X}".format(i))
        if(i < 2**10):
            time.sleep(0.1)
        elif(i < 2**15):
            time.sleep(0.05)
        elif(i < 2**20):
            time.sleep(0.01)
    print("Thank you for watching")

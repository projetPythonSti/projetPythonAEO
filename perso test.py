from datetime import *
import time

def main() :
    print("Hell world")
    t1 = datetime.now()
    time.sleep(5)
    t2 = datetime.now()
    delta = t2 - t1
    print(delta)
    return 0

main()
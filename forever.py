# Run forever

import time
import threading
import maya.utils as utils

def background(func, interval=1):
    """ Run function over and over in background """
    block = threading.Semaphore()

    def run2():
        block.release()
        func()

    def run1():
        while True:
            block.acquire()
            utils.executeDeferred(lambda: cmds.scriptJob(ro=True, ie=run2))
            time.sleep(interval)

    threading.Thread(target=run1).start()

if __name__ == '__main__':

    def test():
        print "HELLO!"
    background(test)

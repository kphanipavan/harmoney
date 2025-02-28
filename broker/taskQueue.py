"""
Task queue manager class, courtesy of Shashwat Kumar
https://medium.com/@shashwat_ds/a-tiny-multi-threaded-job-queue-in-30-lines-of-python-a344c3f3f7f0

Later modified by Phani Pavan K to meet PEP8.1.
Stage 2 modifications include adding multiprocessing for scale up.
"""

import queue
from threading import Thread
from multiprocessing import Process
import time

class TaskQueue(queue.Queue):
    def __init__(self, num_workers=1):
        queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.startWorkers()

    def addTask(self, task, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        self.put((task, args, kwargs))

    def startWorkers(self):
        for _ in range(self.num_workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            item, args, kwargs = self.get()
            p=Process(target=item, args=args, kwargs=kwargs)
            p.start()
            p.join()
            self.task_done()

if __name__ == "__main__":
    testQueue = TaskQueue(4)

    def printer(x):
        for i in range(3):
            print(x)
            time.sleep(1)

    for i in range(10):
        testQueue.addTask(printer, f"Task {i}")
        print(f"Added task {i}")
    print("Done adding tasks to the queue")
    testQueue.join()

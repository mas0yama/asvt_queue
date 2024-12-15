import os
import time

UNIX_TIME_30 = 30 * 60 * 1000


class Queue:
    class Entry:
        def __init__(self, tag, path_to_photo, timestamp):
            self.photo = path_to_photo
            self.tag = tag
            self.timestamp = timestamp

    def __init__(self):
        self.queue = []

    def enqueue(self, tag, path_to_photo, timestamp=0):
        """
        Return codes of enqueue:
        0x00 - success
        0x01 - error
        0x02 - entry exists
        """

        self.queue.append(Queue.Entry(tag, path_to_photo, timestamp))

    def dequeue(self):
        entry = self.queue.pop(0)
        return entry

    def remove_entry(self, entry ):
        self.queue.remove(entry)
        print("Removed entry from queue")
        os.system("rm "+entry.photo)

    def remove_by_tag(self, tag):
        for entry in self.queue:
            if entry.tag == tag:
                self.queue.remove(entry)


    def __iter__(self):
        return iter(self.queue)

def update_queue(queue: Queue):
    cur_time = time.time()
    for entry in queue.queue:
        if cur_time - entry.timestamp >= 50:
            queue.remove_entry(entry)

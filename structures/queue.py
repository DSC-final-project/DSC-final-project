from collections import deque

from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, order):
        self.queue.append(order)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def peek(self):
        if self.queue:
            return self.queue[0]
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)
 
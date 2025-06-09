import heapq


class PriorityQueue:
    def __init__(self, capacity):
        self.heap = []
        self.capacity = capacity

    def push(self, order):
        if len(self.heap) < self.capacity:
            heapq.heappush(self.heap, (order.expected_completion_time, order))
            return True
        return False

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        return None

    def peek(self):
        if self.heap:
            return self.heap[0][1]
        return None

    def __len__(self):
        return len(self.heap)

    def reorder(self):
        heapq.heapify(self.heap)

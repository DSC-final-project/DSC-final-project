import heapq


class PriorityQueue:
    def __init__(self, capacity):
        self.heap = []
        self.capacity = capacity

    def push(self, item_tuple): # item_tuple is (priority, data, ...)
        if len(self.heap) < self.capacity:
            heapq.heappush(self.heap, item_tuple)
            return True
        return False

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap) # Returns the full tuple
        return None

    def peek(self):
        if self.heap:
            return self.heap[0] # Returns the full tuple
        return None

    def __len__(self):
        return len(self.heap)

    def reorder(self): # This might be needed if priorities change externally
        heapq.heapify(self.heap)
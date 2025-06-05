from structures.heap import PriorityQueue
from structures.queue import Queue
from core.menu import MenuItem


class Order:
    def __init__(self, order_id: int, menu: MenuItem, order_time: int):
        self.order_id = order_id
        self.menu = menu
        self.order_time = order_time
        self.start_time = None
        self.estimated_finish_time = None



class OrderManager:
    def __init__(self, menu_manager, capacity=20):
        self.menu_manager = menu_manager
        self.priority_queue = PriorityQueue(capacity)
        self.waiting_queue = Queue()
        self.order_counter = 1
        self.orders = {}

    def create_order(self, menu_name, time):
        menu = self.menu_manager.menu_items.get(menu_name)
        order = Order(self.order_counter, menu, time)
        order.start_time = time
        order.estimated_finish_time = time + menu.cook_time

        if not self.priority_queue.push(order):
            self.waiting_queue.enqueue(order)

        self.orders[self.order_counter] = order
        self.order_counter += 1

    def update_order(self, order_id, new_menu_name) -> bool :
        # 구현: 기존 큐에서 제거 후 재삽입
        # if queue안에 있으면 바꾸고 return true
        # else 이미 heap으로 들어갔으면 return false
        pass

    def delete_order(self, order_id):
        # 구현: 큐에서 제거 및 재정렬
        pass

    def print_order(self, t):
        #Queue, Heap 상황 print

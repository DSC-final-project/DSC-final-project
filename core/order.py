from structures.heap import PriorityQueue
from structures.queue import Queue
from core.menu import MenuItem, MenuManager

class Order:
    def __init__(self, order_id: int, menu: MenuItem, order_time: int):
        '''
        메뉴를 order에 묶어만 놓고, 개별적으로 priority queue에 넣으면서 관리 예정
        주문이 들어오면 Queue에는 동일 주문 기준 시간이 가장 오래걸리는 것부터 정렬하여 동시에 넣기
        이를 통해 Priority queue에 들어가는 애들을 긴것 부터 넣어서 최대한 대기 시간이 짧도록 관리 가능

        order_id - 주문 번호
        order_time - 주문 시점
        start_time - 메뉴 별 조리 시작 시점
        menu_list - 메뉴 목록
        estimanted_finish_time - 메뉴 별 예상 완료 시점
        '''
        self.order_id = order_id
        self.order_time = order_time
        self.menu_list = []
        self.start_time = []
        self.estimated_finish_time = None

class OrderManager:
    def __init__(self, MenuManager, capacity=20):
        self.menu_manager = MenuManager
        # self.priority_queue = PriorityQueue(capacity)
        # self.waiting_queue = Queue()
        self.order_counter = 1
        self.orders = {}

    def create_order(self, order_menu_list):
        '''
        입력받은 주문의 목록을 Order라는 객체에 담기
        메뉴 목록을 나누고, 조리 시간을 기준으로 내림차순 정렬하고,
        메뉴 리스트를 생성하여 관리
        '''
        print('hi')
        # menu = self.menu_manager.menu_items.get(menu_name)
        # order = Order(self.order_counter, menu, time)
        # order.start_time = time
        # order.estimated_finish_time = time + menu.cook_time

        # if not self.priority_queue.push(order):
        #     self.waiting_queue.enqueue(order)

        # self.orders[self.order_counter] = order
        # self.order_counter += 1

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
        pass
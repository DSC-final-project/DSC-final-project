from structures.heap import PriorityQueue
from structures.queue import Queue
from tabulate import tabulate
import heapq # For OrderManager.delete_order

class Order:
    def __init__(self, order_id: int, order_time: int):
        '''
        메뉴를 order에 묶어만 놓고, 개별적으로 priority queue에 넣으면서 관리 예정
        주문이 들어오면 Queue에는 동일 주문 기준 시간이 가장 오래걸리는 것부터 정렬하여 동시에 넣기
        이를 통해 Priority queue에 들어가는 애들을 긴것 부터 넣어서 최대한 대기 시간이 짧도록 관리 가능

        order_id - 주문 번호
        order_time - 주문 시점
        menu_items - MenuItem 객체들의 리스트 (조리 시간 긴 순으로 정렬됨)
        item_status - 각 메뉴 아이템의 상태 ('waiting', 'cooking', 'completed')
        item_cook_start_time - 각 메뉴 아이템의 조리 시작 시간
        item_remaining_cook_time - 각 메뉴 아이템의 남은 조리 시간
        estimated_completion_time - 전체 주문의 예상 완료 시간
        actual_completion_time - 전체 주문의 실제 완료 시간
        status - 전체 주문의 상태 ('pending', 'in_progress', 'ready', 'completed')
        '''
        self.order_id = order_id
        self.order_time = order_time
        self.menu_items = []
        self.item_status = []
        self.item_cook_start_time = []
        self.item_remaining_cook_time = []
        self.estimated_completion_time = None
        self.actual_completion_time = None
        self.status = 'pending'

    def update_order_status_and_estimates(self, current_time):
        """OrderManager가 tick마다 호출하여 주문의 전체 상태와 예상 완료 시간을 업데이트합니다."""
        if not self.menu_items:
            self.status = 'completed'
            self.estimated_completion_time = self.order_time
            self.actual_completion_time = self.order_time
            return

        all_items_completed = True
        max_item_finish_time = self.order_time # 가장 늦게 끝나는 아이템의 완료 시간

        for i in range(len(self.menu_items)):
            if self.item_status[i] != 'completed':
                all_items_completed = False
                if self.item_status[i] == 'cooking':
                    # 현재 조리 중인 아이템의 예상 완료 시간
                    item_finish_time = self.item_cook_start_time[i] + self.menu_items[i].cook_time
                    max_item_finish_time = max(max_item_finish_time, item_finish_time)
                else: # 'waiting'
                    # 대기 중인 아이템은 OrderManager가 슬롯 할당 시 예상 시간을 계산해야 함
                    # 여기서는 단순화를 위해 현재 시간 기준으로 매우 러프하게 설정 (실제로는 더 복잡)
                    max_item_finish_time = float('inf') # 정확한 예측 불가 표시
                    break # 하나라도 대기 중이면 정확한 전체 예상 시간 계산 어려움
            else: # 'completed'
                item_finish_time = self.item_cook_start_time[i] + self.menu_items[i].cook_time
                max_item_finish_time = max(max_item_finish_time, item_finish_time)

        if all_items_completed:
            self.status = 'ready' # 모든 아이템 조리 완료
            if not self.actual_completion_time:
                self.actual_completion_time = max_item_finish_time
            self.estimated_completion_time = self.actual_completion_time
        elif any(s == 'cooking' for s in self.item_status):
            self.status = 'in_progress'
            self.estimated_completion_time = max_item_finish_time if max_item_finish_time != float('inf') else None
        else: # 모든 아이템이 'waiting' (또는 주문 자체가 'pending')
            self.status = 'pending'
            self.estimated_completion_time = None # 아직 시작 전이므로 예상 시간 계산 불가


class OrderManager:
    def __init__(self, menu_manager, cooking_slots_capacity=10): # 기본 10개의 조리 슬롯
        self.menu_manager = menu_manager
        self.cooking_slots = PriorityQueue(cooking_slots_capacity) # (finish_time, order_id, item_idx) 저장
        self.waiting_orders_queue = Queue() # 처리 대기중인 order_id 저장
        self.order_counter = 1
        self.orders = {} # {order_id: Order_instance}
        self.current_time = 0 # TimeStepper에 의해 업데이트됨

    def set_current_time(self, time: int):
        self.current_time = time

    def create_order(self, order_menu_list_details, order_time_received: int):
        '''
        입력받은 주문의 목록을 Order라는 객체에 담기
        메뉴 목록을 나누고, 조리 시간을 기준으로 내림차순 정렬하고,
        메뉴 리스트를 생성하여 관리

        Input
        ; order_menu_list_details - [{MenuItem_object: count}, {MenuItem_object: count}, ...]
        ; order_time_received - 주문이 시스템에 접수된 시간 (tick)
        '''
        current_order_id = self.order_counter
        new_order = Order(order_id=current_order_id, order_time=order_time_received)

        processed_menu_items = []
        for item_dict in order_menu_list_details:
            for menu_item, count in item_dict.items():
                for _ in range(count):
                    processed_menu_items.append(menu_item)
        
        # cook_time을 기준으로 내림차순 정렬
        processed_menu_items.sort(key=lambda item: item.cook_time, reverse=True)
        
        new_order.menu_items = processed_menu_items
        item_count = len(processed_menu_items)
        new_order.item_status = ['waiting'] * item_count
        new_order.item_cook_start_time = [None] * item_count
        new_order.item_remaining_cook_time = [item.cook_time for item in processed_menu_items]

        self.orders[current_order_id] = new_order
        self.waiting_orders_queue.enqueue(current_order_id)
        self.order_counter += 1
        print(f"  Time {order_time_received}: Order {current_order_id} created with {item_count} items. Added to waiting queue.")
        self.schedule_new_items_to_cook(order_time_received) # 생성 즉시 스케줄링 시도
        return current_order_id

    def handle_cooking_completions(self, current_time: int):
        """조리 중인 아이템들의 완료 여부를 확인하고 상태를 업데이트합니다."""
        print(f"  OrderManager: Checking cooking completions at time {current_time}.")
        # completed_items_info = [] # (order_id, item_idx) # Not strictly needed if just updating
        
        temp_cooking_items = []
        while not self.cooking_slots.is_empty():
            finish_time, order_id, item_idx = self.cooking_slots.peek()
            order = self.orders[order_id]

            if current_time >= finish_time:
                self.cooking_slots.pop() 
                order.item_status[item_idx] = 'completed'
                order.item_remaining_cook_time[item_idx] = 0
                print(f"    Item '{order.menu_items[item_idx].name}' (Order {order_id}, ItemIdx {item_idx}) COMPLETED.")

                if all(s == 'completed' for s in order.item_status):
                    order.status = 'ready'
                    order.actual_completion_time = current_time 
                    print(f"    >>> Order {order_id} is READY! <<<")
            else:
                temp_cooking_items.append((finish_time, order_id, item_idx)) 
                self.cooking_slots.pop() 
        
        for item_tuple in temp_cooking_items:
            self.cooking_slots.push(item_tuple)
            
    def schedule_new_items_to_cook(self, current_time: int):
        """대기 중인 주문들의 아이템을 빈 조리 슬롯에 할당합니다."""
        print(f"  OrderManager: Scheduling new items at time {current_time}.")
        
        can_schedule_more = True
        orders_checked_in_queue = 0 
        
        while len(self.cooking_slots) < self.cooking_slots.capacity and \
              not self.waiting_orders_queue.is_empty() and \
              can_schedule_more and \
              orders_checked_in_queue < len(self.waiting_orders_queue):
            
            order_id_to_process = self.waiting_orders_queue.peek()
            order = self.orders[order_id_to_process]
            
            item_scheduled_this_iteration = False
            for item_idx, status in enumerate(order.item_status):
                if status == 'waiting':
                    if len(self.cooking_slots) < self.cooking_slots.capacity:
                        menu_item_obj = order.menu_items[item_idx]
                        
                        order.item_status[item_idx] = 'cooking'
                        order.item_cook_start_time[item_idx] = current_time
                        
                        expected_finish_time = current_time + menu_item_obj.cook_time
                        self.cooking_slots.push((expected_finish_time, order_id_to_process, item_idx))
                        
                        print(f"    Item '{menu_item_obj.name}' (Order {order_id_to_process}, ItemIdx {item_idx}) STARTS cooking. Est.Finish: {expected_finish_time}.")
                        item_scheduled_this_iteration = True
                        if order.status == 'pending': 
                            order.status = 'in_progress'
                    else:
                        can_schedule_more = False 
                        break 
            
            orders_checked_in_queue += 1
            if all(s != 'waiting' for s in order.item_status):
                self.waiting_orders_queue.dequeue()
            elif not item_scheduled_this_iteration and not can_schedule_more:
                break 

    def update_all_order_details(self, current_time: int):
        """모든 주문의 상태 및 예상 시간을 업데이트합니다 (주로 표시용)."""
        print(f"  OrderManager: Updating all order details for time {current_time}.")
        for order in self.orders.values():
            if order.status not in ['ready', 'completed']: 
                order.update_order_status_and_estimates(current_time)

    def get_order_status_details(self, order_id: int) -> str:
        if order_id not in self.orders:
            return f"Order ID {order_id} not found."
        
        order = self.orders[order_id]
        order.update_order_status_and_estimates(self.current_time) 

        details = [
            f"Order ID: {order.order_id}",
            f"  Status: {order.status}",
            f"  Order Time: {order.order_time}",
            f"  Est. Completion: {order.estimated_completion_time if order.estimated_completion_time is not None else 'N/A'}",
            f"  Actual Completion: {order.actual_completion_time if order.actual_completion_time is not None else 'N/A'}",
            "  Items:"
        ]
        for i, menu_item in enumerate(order.menu_items):
            item_detail = f"    - {menu_item.name}: {order.item_status[i]}"
            if order.item_status[i] == 'cooking':
                start = order.item_cook_start_time[i]
                finish = start + menu_item.cook_time
                item_detail += f" (Started: {start}, Finishes: {finish}, Remaining: {finish - self.current_time})"
            elif order.item_status[i] == 'completed':
                start = order.item_cook_start_time[i]
                finish = start + menu_item.cook_time
                item_detail += f" (Cooked: {start}-{finish})"
            details.append(item_detail)
        return "\n".join(details)

    def print_all_orders_summary(self):
        print(f"\n--- Orders Summary at Time {self.current_time} ---")
        if not self.orders:
            print("No orders in the system.")
            return

        headers = ["Order ID", "Status", "Order Time", "Est. Finish", "Actual Finish", "Items"]
        table_data = []
        for order_id in sorted(self.orders.keys()):
            order = self.orders[order_id]
            order.update_order_status_and_estimates(self.current_time) 
            num_items = len(order.menu_items)
            items_summary = f"{sum(1 for s in order.item_status if s == 'completed')}/{num_items} done"
            table_data.append([
                order.order_id,
                order.status,
                order.order_time,
                order.estimated_completion_time if order.estimated_completion_time is not None and order.estimated_completion_time != float('inf') else "N/A",
                order.actual_completion_time if order.actual_completion_time is not None else "N/A",
                items_summary
            ])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        print("\n--- Cooking Slots ---")
        if self.cooking_slots.is_empty():
            print("All cooking slots are free.")
        else:
            active_cooking_items = sorted(list(self.cooking_slots.heap)) 
            for finish_time, o_id, item_idx in active_cooking_items:
                item_order = self.orders[o_id]
                menu_item = item_order.menu_items[item_idx]
                print(f"  Slot: Order {o_id}, Item '{menu_item.name}' (Idx {item_idx}). Finishes at {finish_time}. Started at {item_order.item_cook_start_time[item_idx]}.")
        
        print("\n--- Waiting Orders Queue ---")
        if self.waiting_orders_queue.is_empty():
            print("Waiting queue is empty.")
        else:
            print(f"  Order IDs in waiting queue: {[q_order_id for q_order_id in list(self.waiting_orders_queue.queue)]}")
        print("--------------------------------\n")

    def update_order(self, order_id, new_menu_name) -> bool:
        print(f"Warning: update_order for order {order_id} is not fully implemented for timed simulation.")
        return False

    def delete_order(self, order_id_to_delete: int) -> bool:
        print(f"Attempting to delete Order ID: {order_id_to_delete} at time {self.current_time}")
        if order_id_to_delete not in self.orders:
            print(f"  Order {order_id_to_delete} not found.")
            return False

        # order = self.orders[order_id_to_delete] # Not strictly needed if just removing

        new_cooking_heap = []
        items_removed_from_cooking = 0
        while not self.cooking_slots.is_empty():
            item_tuple = self.cooking_slots.pop() 
            if item_tuple[1] == order_id_to_delete: 
                items_removed_from_cooking +=1
            else:
                new_cooking_heap.append(item_tuple)
        
        self.cooking_slots.heap = new_cooking_heap
        heapq.heapify(self.cooking_slots.heap) 
        if items_removed_from_cooking > 0:
             print(f"  Removed {items_removed_from_cooking} items of Order {order_id_to_delete} from cooking slots.")

        new_waiting_queue = Queue()
        item_removed_from_waiting = False
        while not self.waiting_orders_queue.is_empty():
            oid = self.waiting_orders_queue.dequeue()
            if oid == order_id_to_delete:
                item_removed_from_waiting = True
            else:
                new_waiting_queue.enqueue(oid)
        self.waiting_orders_queue = new_waiting_queue
        if item_removed_from_waiting:
            print(f"  Order {order_id_to_delete} removed from waiting queue.")

        del self.orders[order_id_to_delete]
        print(f"  Order {order_id_to_delete} deleted from main order list.")
        # Attempt to schedule new items as slots might have opened up
        self.schedule_new_items_to_cook(self.current_time)
        return True

    def print_order(self): # Kept for compatibility with user_services, but uses new summary
        '''
        현재 시스템에 저장된 모든 주문 목록을 출력합니다.
        각 주문의 ID와 해당 주문에 포함된 메뉴 목록을 tabulate를 사용하여 표시합니다.
        '''
        if not self.orders:
            print("현재 주문 내역이 없습니다.\n")
            return
        self.print_all_orders_summary()

    def print_order_with_previous_page(self): # Kept for compatibility, uses new summary
        '''
        print인데 뒤로가기 버튼도 출력
        '''
        if not self.orders:
            print("현재 주문 내역이 없습니다.\n")
            return
        self.print_all_orders_summary()
        # The "Previous Page" part of the UI should be handled by the calling function in user_services
        # For example, after this print, user_services can print its own "Previous Page" option.
from structures.heap import PriorityQueue
from structures.queue import Queue
from tabulate import tabulate
import heapq # For OrderManager.delete_order
from collections import Counter

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
        status - 전체 주문의 상태 ('pending', 'in_progress', 'ready', 'completed') #####################?? ready completed 차이가 뭐지 
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
        if not self.menu_items: #?
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

    def get_item_details_for_modification_display(self):
        """
        Returns a list of tuples for display in user_services update menu.
        Each tuple: (item_name, item_status, original_index_in_menu_items_list, item_price)
        """
        details = []
        for i, menu_item in enumerate(self.menu_items):
            # Storing original_index (i) is useful for mapping display choice back to actual item
            details.append((menu_item.name, self.item_status[i], i, menu_item.price))
        return details


class OrderManager:
    def __init__(self, menu_manager, cooking_slots_capacity=10): # 기본 10개의 조리 슬롯
        self.menu_manager = menu_manager
        self.cooking_slots = PriorityQueue(cooking_slots_capacity) # (finish_time, order_id, item_idx) 저장
        self.waiting_orders_queue = Queue() # 처리 대기중인 order_id 저장
        self.order_counter = 0 # 들어온 주문 수
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
        self.order_counter += 1
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
        self.schedule_new_items_to_cook(order_time_received) # 생성 즉시 스케줄링 시도
        return current_order_id
    

    def diff_orders(self, org_order_dic, new_order_dic):
        '''
        Return : [[변경1], [변경2], ...]
        메뉴 변경이면 - [0, 이전메뉴, 이후메뉴]
        메뉴 수량 감소이면 - [1, 대상메뉴, 변경수량(-n)]
        '''

        removed = {}
        added   = {}
        for name in set(org_order_dic) | set(new_order_dic):
            if name not in self.menu_manager.menu_items:
                print(f"[주문변경] X {name}는 없는 메뉴입니다")
                continue
            old = org_order_dic.get(name, 0)
            new = new_order_dic.get(name, 0)
            if new < old:
                removed[name] = old - new
            elif new > old:
                added[name] = new - old
        
        changes = []
        for rem_name, rem_qty in list(removed.items()):
            if rem_qty <= 0:
                continue
            for add_name, add_qty in list(added.items()):
                if add_qty <= 0:
                    continue
                qty = min(rem_qty, add_qty)
                changes.append([0, rem_name, add_name])
                removed[rem_name] -= qty
                added[add_name]   -= qty
                rem_qty = removed[rem_name]
                if rem_qty == 0:
                    break
        
        for name, qty in removed.items():
            if qty > 0:
                changes.append([1, name, -qty])
        for name, qty in added.items():
            if qty > 0:
                print(f"[주문변경] X 메뉴를 추가하시려면 새 주문을 접수하여 주시기 바랍니다")
        
        return changes
    

    def update_order(self, order_id_to_update, new_order) : 

        order = self.orders.get(order_id_to_update)
        if not order:
            return "접수되지 않은 주문입니다"

        if order.status =='ready':
            return "이미 제조완료된 주문입니다"
        
        if order.status == 'pending': # 아직 아무것도 시작하기 전이므로 그냥 입력받은걸로 대체
            self.orders[order_id_to_update] = new_order
        else: # in_progress or completed
            org_order_dic = Counter(order.menu_items)
            new_order_dic = {name: qty for name, qty in new_order}
            changes = self.diff_orders(org_order_dic, new_order_dic)
            
            for change in changes:
                if change[0] == 0:
                    old_menu = change[1]
                    new_menu = change[2]
                    for idx, menu in enumerate(order.menu_items):
                        if menu == old_menu & order.item_status[idx] == 'waiting':
                            order.menu_items[idx] = new_menu
                            order.item_remaining_cook_time[idx] = self.menu_manager.menu_items[new_menu].cook_time
                            break
                elif change[0] == 1:
                    target_menu = change[1]
                    n = change[2]
                    count = 0
                    for idx, menu in enumerate(order.menu_items):
                        if menu == target_menu & order.item_status[idx] == 'waiting':
                            del order.menu_items[idx] 
                            del order.item_status[idx] 
                            del order.item_cook_start_time[idx]
                            del order.item_remaining_cook_time[idx] 
                            count += 1
                            if count == n:
                                break
                else:
                    print("Error: 정의되지 않은 update")
        order.update_order_status_and_estimates(self.current_time)

        return order
    

    def delete_order(self, order_id_to_delete: int) -> tuple[bool, int]:
        """
        Deletes an order from the system.
        Returns: (success_bool, refund_amount_int)
        """

        if order_id_to_delete not in self.orders:
            return "접수되지 않은 주문입니다"

        order_to_delete = self.orders[order_id_to_delete]
        order_to_delete.update_order_status_and_estimates(self.current_time) # Ensure status is current

        if order_to_delete.status in ['in_progress', 'completed', 'ready']: #남는 경우는 pending 밖에 없음 
            return "조리가 이미 시작되어 취소가 불가능합니다"

        # Calculate refund amount (total price of all items in the order)
        refund_amount = sum(item.price for item in order_to_delete.menu_items)

        new_waiting_queue = Queue()
        while not self.waiting_orders_queue.is_empty():
            oid = self.waiting_orders_queue.dequeue()
            if oid == order_id_to_delete:
                continue
            else:
                new_waiting_queue.enqueue(oid)
        self.waiting_orders_queue = new_waiting_queue

        del self.orders[order_id_to_delete]
        return refund_amount

    def get_order_status_details(self, order_id: int, user_view: bool = False) -> str:
        if order_id not in self.orders:
            return f"Order ID {order_id} not found."
        
        order = self.orders[order_id]
        order.update_order_status_and_estimates(self.current_time) 

        details = [f"Order ID: {order.order_id}"]

        if not user_view:
            details.append(f"  Status: {order.status}")
        
        details.extend([
            f"  Order Time: {order.order_time}",
            f"  Est. Completion: {order.estimated_completion_time if order.estimated_completion_time is not None else 'N/A'}",
        ])

        if not user_view:
            details.append(f"  Actual Completion: {order.actual_completion_time if order.actual_completion_time is not None else 'N/A'}")

        details.append("  Items:")
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
            
            items_display_list = []
            if order.menu_items:
                num_total_items = len(order.menu_items)
                num_completed_items = sum(1 for s in order.item_status if s == 'completed')
                items_display_list.append(f"{num_completed_items}/{num_total_items} done")
                for i, menu_item_obj in enumerate(order.menu_items):
                    items_display_list.append(f"  - {menu_item_obj.name}: {order.item_status[i]}")
            else:
                items_display_list.append("No items (Order Empty/Deleted)")
            
            table_data.append([
                order.order_id,
                order.status,
                order.order_time,
                order.estimated_completion_time if order.estimated_completion_time is not None and order.estimated_completion_time != float('inf') else "N/A",
                order.actual_completion_time if order.actual_completion_time is not None else "N/A",
                "\n".join(items_display_list) # 각 아이템 정보를 개행으로 연결
            ])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print()

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




    def handle_cooking_completions(self, current_time: int):
        """
        Heap에서 조리 완료된 아이템들 확인
        """
        
        while not self.cooking_slots.is_empty():
            self.cooking_slots.reorder()
            finish_time, order_id, item_idx = self.cooking_slots.peek()
            order = self.orders[order_id]

            if current_time >= finish_time:
                self.cooking_slots.pop() 
                order.item_status[item_idx] = 'completed'
                order.item_remaining_cook_time[item_idx] = 0
                # print(f"    Item '{order.menu_items[item_idx].name}' (Order {order_id}, ItemIdx {item_idx}) COMPLETED.")

                if all(s == 'completed' for s in order.item_status):
                    order.status = 'ready'
                    order.actual_completion_time = current_time 
                    order_dic = Counter(order.menu_items)
                    items = ", ".join(f"{name}{qty}" for name, qty in order_dic.items())
                    print(f"[제조완료] 주문번호 {order_id} - {items} ")
                    # print(f"    >>> Order {order_id} is READY! <<<")
            else:
                break 
            

    def schedule_new_items_to_cook(self, current_time: int):
        """대기 중인 주문들의 아이템을 빈 조리 슬롯에 할당합니다."""
        # print(f"  OrderManager: Scheduling new items at time {current_time}.")

        # To prevent an infinite loop if an order at the head of the queue
        # cannot be processed (e.g., no items scheduled for it) and is not dequeued,
        # this tracks the ID of such an order. If we see it again immediately without progress, we stop.
        stuck_order_id_at_head = None

        while len(self.cooking_slots) < self.cooking_slots.capacity and \
              not self.waiting_orders_queue.is_empty():

            order_id_to_process = self.waiting_orders_queue.peek()

            if stuck_order_id_at_head == order_id_to_process:
                # We've already tried this order in this scheduling cycle, made no progress,
                # and it's still at the head. Break to prevent an infinite loop.
                # print(f"    Order ID {order_id_to_process} is still at head with no progress made in this cycle. Breaking scheduling.")
                break

            order = self.orders[order_id_to_process]
            # print(f"    Considering Order ID: {order_id_to_process} (Status: {order.status}, Items: {len(order.menu_items)})")

            item_scheduled_this_iteration = False
            for item_idx, status in enumerate(order.item_status):
                if status == 'waiting':
                    if len(self.cooking_slots) < self.cooking_slots.capacity:
                        menu_item_obj = order.menu_items[item_idx]
                        order.item_status[item_idx] = 'cooking'
                        order.item_cook_start_time[item_idx] = current_time
                        
                        expected_finish_time = current_time + menu_item_obj.cook_time
                        self.cooking_slots.push((expected_finish_time, order_id_to_process, item_idx))
                        
                        # print(f"    Item '{menu_item_obj.name}' (Order {order_id_to_process}, ItemIdx {item_idx}) STARTS cooking. Est.Finish: {expected_finish_time}.")
                        item_scheduled_this_iteration = True
                        if order.status == 'pending': 
                            order.status = 'in_progress'
                        stuck_order_id_at_head = None # Progress was made, so reset the stuck flag
                    else:
                        # print(f"      No more cooking slots during Order {order_id_to_process}. Breaking item loop.")
                        break 

            if all(s != 'waiting' for s in order.item_status):
                # All items for this order are now cooking or completed
                self.waiting_orders_queue.dequeue()
                # print(f"    All items for Order {order_id_to_process} are now scheduled/completed. Dequeued.")
                stuck_order_id_at_head = None # Head of queue changed
            elif not item_scheduled_this_iteration:
                # No items were scheduled for this order in this pass.
                # It remains at the head. Mark it as potentially stuck.
                # print(f"    No items scheduled for Order {order_id_to_process} in this pass. It remains at head.")
                stuck_order_id_at_head = order_id_to_process
            else:
                # Items were scheduled, but the order is not fully done. It remains at head.
                # Since progress was made, reset stuck_order_id_at_head.
                stuck_order_id_at_head = None

    def update_all_order_details(self, current_time: int):
        """모든 주문의 상태 및 예상 시간을 업데이트합니다 (주로 표시용)."""
        # print(f"  OrderManager: Updating all order details for time {current_time}.")
        for order in self.orders.values():
            if order.status not in ['ready', 'completed']: 
                order.update_order_status_and_estimates(current_time)



    ############# for user_services.py ##############

    def _remove_item_from_cooking_slot_by_order_item_idx(self, order_id: int, item_idx_in_order: int):
        """
        Removes a specific item of an order from the cooking_slots.
        Returns True if removed, False otherwise.
        """
        item_found_and_removed = False
        new_cooking_heap = []
        # Directly access and rebuild the heap
        current_heap = list(self.cooking_slots.heap) 
        self.cooking_slots.heap.clear()

        for slot_item_tuple in current_heap:
            _slot_finish_time, slot_order_id, slot_item_idx = slot_item_tuple
            if slot_order_id == order_id and slot_item_idx == item_idx_in_order:
                item_found_and_removed = True
                # print(f"    DEBUG: Item (Order {order_id}, ItemIdx {item_idx_in_order}) removed from cooking slot.")
            else:
                new_cooking_heap.append(slot_item_tuple)
        
        self.cooking_slots.heap = new_cooking_heap
        heapq.heapify(self.cooking_slots.heap) 
        if item_found_and_removed:
            # print(f"  Item (Order {order_id}, ItemIdx {item_idx_in_order}) was cooking and has been removed from slot.")
            pass
        return item_found_and_removed

    def _adjust_cooking_slot_indices_after_delete(self, order_id_affected: int, deleted_item_original_idx: int):
        """
        After an item is deleted from an order's menu_items list at deleted_item_original_idx,
        this method updates the item_idx for other items of the SAME order
        that are still in cooking_slots and had an original index
        greater than the deleted item_original_idx.
        Their stored item_idx needs to be decremented by 1.
        """
        # print(f"    DEBUG: Adjusting cooking slot indices for Order {order_id_affected} after deletion of item at original index {deleted_item_original_idx}.")
        rebuild_heap = False
        new_heap_elements = []
        
        current_heap = list(self.cooking_slots.heap)
        self.cooking_slots.heap.clear() # Prepare to rebuild

        for slot_tuple in current_heap:
            finish_time, order_id_in_slot, item_idx_in_slot = slot_tuple
            if order_id_in_slot == order_id_affected and item_idx_in_slot > deleted_item_original_idx:
                new_item_idx = item_idx_in_slot - 1
                new_heap_elements.append((finish_time, order_id_in_slot, new_item_idx))
                rebuild_heap = True
            else:
                new_heap_elements.append(slot_tuple)
        
        self.cooking_slots.heap = new_heap_elements
        if rebuild_heap: # Only heapify if changes were made
            heapq.heapify(self.cooking_slots.heap)

    def _ensure_order_in_waiting_queue(self, order_id: int):
        """
        Ensures an order is in the waiting queue, typically at the end if re-added.
        This is called after modifications that might introduce 'waiting' items or change priority.
        """
        order = self.orders.get(order_id)
        if not order:
            return

        # Remove from waiting queue if it exists, to re-add at the end
        current_q_list = list(self.waiting_orders_queue.queue) # Get a list copy
        self.waiting_orders_queue.queue.clear() # Clear original deque
        
        order_was_in_queue = False
        for oid_in_q in current_q_list:
            if oid_in_q == order_id:
                order_was_in_queue = True
            else:
                self.waiting_orders_queue.enqueue(oid_in_q) # Re-add other orders
        
        # If the order has waiting items or is pending, and not yet completed/ready, add it to the queue.
        if order.menu_items and order.status not in ['ready', 'completed'] and \
           (order.status == 'pending' or any(s == 'waiting' for s in order.item_status)):
            self.waiting_orders_queue.enqueue(order_id)
            # print(f"    DEBUG: Order {order_id} ensured in waiting queue (was_in_queue: {order_was_in_queue}). Status: {order.status}")

    def modify_specific_item_in_order(self, order_id: int, item_idx_in_order: int, new_menu_item_obj=None, delete_item_flag=False):
        """
        Modifies or deletes a specific item in an order.
        Returns: (success_bool, price_difference_int)
                 price_difference = new_price - old_price (negative for refund if deleted/cheaper)
        """
        if order_id not in self.orders:
            # print(f"  Error: Order {order_id} not found for modification.")
            return False, 0

        order = self.orders[order_id]

        if not (0 <= item_idx_in_order < len(order.menu_items)):
            # print(f"  Error: Invalid item index {item_idx_in_order} for Order {order_id}.")
            return False, 0

        original_item_status = order.item_status[item_idx_in_order]
        original_menu_item = order.menu_items[item_idx_in_order]
        price_difference = 0

        if original_item_status == 'completed':
            # print(f"  Error: Item '{original_menu_item.name}' in Order {order_id} (Idx {item_idx_in_order}) is 'completed' and cannot be modified.")
            return False, 0

        if original_item_status == 'cooking':
            self._remove_item_from_cooking_slot_by_order_item_idx(order_id, item_idx_in_order)
            # Item state will be reset to 'waiting'

        if delete_item_flag:
            price_difference = -original_menu_item.price # Refund for the deleted item
            # print(f"  Deleting item '{original_menu_item.name}' (Original Idx {item_idx_in_order}) from Order {order_id}.")
            
            order.menu_items.pop(item_idx_in_order)
            order.item_status.pop(item_idx_in_order)
            order.item_cook_start_time.pop(item_idx_in_order)
            order.item_remaining_cook_time.pop(item_idx_in_order)

            # Adjust indices for other items of THE SAME ORDER in cooking_slots
            self._adjust_cooking_slot_indices_after_delete(order_id, item_idx_in_order)
            
            if not order.menu_items:
                # print(f"  Order {order_id} is now empty after item deletion.")
                pass
        elif new_menu_item_obj:
            price_difference = new_menu_item_obj.price - original_menu_item.price
            # print(f"  Changing item '{original_menu_item.name}' to '{new_menu_item_obj.name}' in Order {order_id} (Idx {item_idx_in_order}).")
            order.menu_items[item_idx_in_order] = new_menu_item_obj
            order.item_status[item_idx_in_order] = 'waiting' # Changed/modified item goes to waiting
            order.item_cook_start_time[item_idx_in_order] = None
            order.item_remaining_cook_time[item_idx_in_order] = new_menu_item_obj.cook_time
        else:
            # print("  Error: No modification action specified (delete or change) for item.")
            return False, 0

        order.update_order_status_and_estimates(self.current_time)
        self._ensure_order_in_waiting_queue(order_id) # Re-evaluate its position or add if needed
        self.schedule_new_items_to_cook(self.current_time)

        # print(f"  Order {order_id} item modification processed. Price difference: {price_difference}")
        return True, price_difference

    def add_new_item_to_order(self, order_id: int, menu_item_obj_to_add, quantity: int):
        if order_id not in self.orders:
            # print(f"  Error: Order {order_id} not found for adding new item.")
            return False
        
        if not menu_item_obj_to_add or quantity <= 0:
            # print(f"  Error: Invalid menu item or quantity for adding to Order {order_id}.")
            return False

        order = self.orders[order_id]
        # print(f"  Adding {quantity} of '{menu_item_obj_to_add.name}' to Order {order_id}.")
        for _ in range(quantity):
            order.menu_items.append(menu_item_obj_to_add)
            order.item_status.append('waiting')
            order.item_cook_start_time.append(None)
            order.item_remaining_cook_time.append(menu_item_obj_to_add.cook_time)

        if order.status in ['ready', 'completed']: # If order was considered done
            order.status = 'pending' # It's no longer fully ready/completed
            order.actual_completion_time = None # Reset actual completion

        order.update_order_status_and_estimates(self.current_time)
        self._ensure_order_in_waiting_queue(order_id) # Ensure it's (re)queued, likely at the end
        self.schedule_new_items_to_cook(self.current_time)
        return True

    def is_menu_item_active_in_orders(self, menu_item_name_to_check: str) -> bool:
        """
        Checks if a given menu item name is part of any order that is currently
        in the waiting queue or has items cooking in the cooking slots.
        This helps prevent modification/deletion of menu items that are actively being processed.
        """
        # Check orders in the waiting queue
        for order_id_in_waiting_q in list(self.waiting_orders_queue.queue):
            order = self.orders.get(order_id_in_waiting_q)
            if order:
                for item in order.menu_items:
                    if item.name == menu_item_name_to_check:
                        # print(f"DEBUG: Menu item '{menu_item_name_to_check}' found in waiting Order ID {order_id_in_waiting_q}.")
                        return True

        # Check items currently in cooking slots
        for _, order_id_in_cooking, item_idx_in_cooking in list(self.cooking_slots.heap):
            order = self.orders.get(order_id_in_cooking)
            if order and item_idx_in_cooking < len(order.menu_items):
                if order.menu_items[item_idx_in_cooking].name == menu_item_name_to_check:
                    # print(f"DEBUG: Menu item '{menu_item_name_to_check}' found cooking in Order ID {order_id_in_cooking} (Item Idx {item_idx_in_cooking}).")
                    return True
        
        return False
    

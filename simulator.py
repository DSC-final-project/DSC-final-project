import json
from core.menu import MenuManager
from core.order import OrderManager

class TimeStepper:
    def __init__(self, order_manager: OrderManager):
        self.time = 0 # 시뮬레이션 현재 시간 (tick)
        self.order_manager = order_manager

    def step(self):
        """시뮬레이션 시간을 한 단위 증가시키고, OrderManager가 해당 시간의 작업을 처리하도록 합니다."""
        current_processing_time = self.time # 현재 시간의 작업을 처리

        print(f"--- TimeStepper: Processing for time {current_processing_time} ---")
        # OrderManager에 현재 시간 알림
        self.order_manager.set_current_time(current_processing_time)

        # OrderManager의 시간 의존적 로직들을 순차적으로 호출
        self.order_manager.handle_cooking_completions(current_processing_time)
        self.order_manager.schedule_new_items_to_cook(current_processing_time)
        self.order_manager.update_all_order_details(current_processing_time)

        # 그 다음 시간을 증가시켜 다음 step을 준비
        self.time += 1
        # print(f"--- TimeStepper: Time advanced to {self.time} ---") # 상세 로그 필요시 주석 해제


def simulate(file_path: str, menu_mgr: MenuManager, order_mgr: OrderManager, sim: TimeStepper):
    """
    지정된 command 파일에 따라 시뮬레이션을 실행합니다.
    MenuManager, OrderManager, TimeStepper 인스턴스는 외부에서 생성되어 주입됩니다.
    """

    with open(file_path, "r") as f:
        commands = json.load(f)

    max_command_time = 0
    if commands:
        max_command_time = max(cmd.get("time", 0) for cmd in commands)
    
    simulation_duration = max(max_command_time + 20, 30) 

    print(f"--- Simulation Start (File: {file_path}) ---")
    print(f"Total simulation duration: {simulation_duration} ticks")
    # 초기 상태에서 OrderManager의 current_time을 TimeStepper의 초기 시간과 동기화
    order_mgr.set_current_time(sim.time)
    order_mgr.print_all_orders_summary() 

    for _ in range(simulation_duration): # 루프 변수 t는 직접 사용하지 않고 sim.time을 기준으로 함
        current_sim_time = sim.time 
        print(f"\n\n======= Processing Time Step: {current_sim_time} =======")

        for cmd in commands:
            if cmd.get("time") == current_sim_time:
                action = cmd["action"]
                print(f"  Action at time {current_sim_time}: {cmd}")
                if action == "create":
                    menu_name = cmd.get("menu")
                    menu_item_obj = menu_mgr.menu_items.get(menu_name)
                    if menu_item_obj:
                        order_details = [{menu_item_obj: 1}] 
                        new_om_order_id = order_mgr.create_order(order_details, current_sim_time)
                        print(f"    Simulator: Requested creation for '{menu_name}'. OrderManager assigned ID {new_om_order_id}.")
                    else:
                        print(f"    Error: Menu item '{menu_name}' not found for create command.")
                
                elif action == "delete":
                    order_id_to_delete = cmd.get("order_id")
                    if order_id_to_delete is not None:
                        success = order_mgr.delete_order(order_id_to_delete)
                        print(f"    Simulator: Delete action for order_id {order_id_to_delete}. Success: {success}")
                    else:
                        print(f"    Error: 'order_id' missing for delete command.")

                elif action == "update":
                    order_id_to_update = cmd.get("order_id")
                    new_menu_name = cmd.get("menu") # Assuming this is a string name
                    print(f"    Simulator: Update action for order_id {order_id_to_update} to '{new_menu_name}' - (Note: update logic is complex and may be limited).")
                    if order_id_to_update is not None:
                         order_mgr.update_order(order_id_to_update, new_menu_name) 
                elif action == "print": # Assuming print command takes an order_id
                    order_id_to_print = cmd.get("order_id")
                    if order_id_to_print is not None:
                        print(f"    Simulator: Printing details for Order ID {order_id_to_print}")
                        print(order_mgr.get_order_status_details(order_id_to_print))
                    else: # If no order_id, print all
                        print(f"    Simulator: Printing all orders summary.")
                        order_mgr.print_all_orders_summary()
        
        sim.step() 

        order_mgr.print_all_orders_summary()
        
        if current_sim_time >= max_command_time + 10: 
            all_orders_done = True
            if not order_mgr.orders:
                 pass 
            elif not any(o.status not in ['ready', 'completed'] for o in order_mgr.orders.values()):
                 if order_mgr.waiting_orders_queue.is_empty() and order_mgr.cooking_slots.is_empty():
                    print(f"\nAll orders completed and queues are empty at time {current_sim_time}. Ending simulation early.")
                    break
    
    print(f"\n--- Simulation End (after {sim.time} ticks) ---")




if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming simulator.py is in the 'script' directory, and 'assets' is a sibling to 'script'
    # If simulator.py is in the project root, and assets is a subdirectory:
    # command_path = os.path.join(script_dir, 'assets', 'commands.json')
    # Based on your project structure (script folder containing simulator.py, assets folder at root)
    project_root = os.path.join(script_dir, '..') 
    command_path = os.path.join(project_root, 'assets', 'commands.json')
    
    menu_manager = MenuManager()
    # Ensure MenuManager has items, if not loaded by default constructor
    if not menu_manager.menu_items: 
        menu_manager.create_menu("아메리카노", "3", "3000")
        menu_manager.create_menu("카페라떼", "5", "3500")
        menu_manager.create_menu("카푸치노", "5", "4000")
        menu_manager.create_menu("에스프레소", "2", "2500")
        print("Default menu items loaded into MenuManager for simulation.")
    
    order_manager = OrderManager(menu_manager, cooking_slots_capacity=2) 
    time_stepper = TimeStepper(order_manager)

    simulate(command_path, menu_manager, order_manager, time_stepper)
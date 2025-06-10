import json
import time

from core.menu import MenuManager
from core.order import OrderManager

class TimeStepper:
    def __init__(self, order_manager):
        self.time = 0
        self.order_manager = order_manager

    def step(self):
        # 완료된 주문 제거
        # 큐 이동 및 정렬 갱신
        # print current state if needed

        self.order_manager.priority_queue
        self.time += 1



def simulate(file_path, print_flag = False, delay = 1):
    menu_mgr = MenuManager()
    order_mgr = OrderManager(menu_mgr, capacity=20)
    sim = TimeStepper(order_mgr)

    #메뉴 출력
    menu_mgr.print_menu()
    menu = menu_mgr.get_menu()

    with open(file_path, "r") as f:
        commands = json.load(f)

    total_time = max(cmd["time"] for cmd in commands) + max(menu[cmd["menu"]].cook_time for cmd in commands)
    for t in range(total_time):
        
        print(f"\n⏱ {t}분")
        for cmd in commands:
            if cmd["time"] == t:
                action = cmd["action"]
                if action == "create":
                    order_mgr.create_order(cmd["menu"], t)
                    print(f"  접수 완료: 주문번호 {cmd["order_id"]} '{cmd['menu']}' ")
                elif action == "update":
                    org_menu = order_mgr.orders[cmd["order_id"]].menu
                    updated = order_mgr.update_order(cmd["order_id"], cmd["menu"])
                    if updated:
                        print(f"  변경 완료: 주문번호 {cmd['order_id']} 메뉴 '{org_menu}' → '{cmd['menu']}' ")
                    else:
                        print(f"  주문번호 {cmd['order_id']} '{cmd['menu']}'의 제조가 이미 시작되어 변경이 불가능합니다. ")
        sim.step()

        if print_flag:
            print('\n')
            print('-'*15)
            order_mgr.print_order(t)
            print('-'*15)

        print('\n'*5)
        time.sleep(delay)



if __name__ == "__main__":

    command_path = 'assets/commands.json'
    simulate(command_path)
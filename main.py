from core.menu import MenuManager
from core.order import OrderManager
from simulator import TimeStepper

def main():
    menu_mgr = MenuManager()
    order_mgr = OrderManager(menu_mgr, capacity=3)
    sim = TimeStepper(order_mgr)

    # 메뉴 생성
    menu_mgr.create_menu("아메리카노", 3, 3000)
    menu_mgr.create_menu("카페라떼", 5, 4000)

    # 주문 생성
    order_mgr.create_order("아메리카노", sim.time)
    order_mgr.create_order("카페라떼", sim.time)

    # 시간 진행
    sim.step()
    sim.step()

if __name__ == "__main__":
    main()

# Hello World!
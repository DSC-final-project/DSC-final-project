# 구현한 함수 테스트용
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(current_dir, '..')
sys.path.append(main_dir)

import user_services
import core.menu as menu
import core.order as order

test_menu_manager = menu.MenuManager()
test_order_manager = order.OrderManager(test_menu_manager)

main_menu = user_services.main_service_menu(test_menu_manager, test_order_manager)
menu_repeat_flag = True
while menu_repeat_flag:
    menu_repeat_flag = main_menu.main_system()
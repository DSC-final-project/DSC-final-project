# 구현한 함수 테스트용
import user_services
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(current_dir, '..')
sys.path.append(main_dir)

import core.menu as menu

test_menu_manager = menu.MenuManager()
main_menu = user_services.main_service_menu(test_menu_manager)
menu_repeat_flag = True
while menu_repeat_flag:
    menu_repeat_flag = main_menu.main_system()
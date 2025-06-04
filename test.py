# 구현한 함수 테스트용
import core.menu as menu
import user_services

test_menu_manager = menu.MenuManager()
main_menu = user_services.main_service_menu(test_menu_manager)
menu_repeat_flag = True
while menu_repeat_flag:
    menu_repeat_flag = main_menu.main_system()
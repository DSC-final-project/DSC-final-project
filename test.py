# 구현한 함수 테스트용
import core.menu as menu
import user_services

test_menu_manager = menu.MenuManager()
test_menu_manager.print_menu()

# Error case - create_menu
test_menu_manager.create_menu('', 3, 3500)
test_menu_manager.create_menu(71, 3, 3500)
test_menu_manager.create_menu('dasd', -3, 3500)
test_menu_manager.create_menu('asdasd', 3, -3500)

# Example Case
test_menu_manager.create_menu('dd', 3, 3500)
test_menu_manager.print_menu()

# 이런식으로 함수 구성해서 메뉴 CRUD 진행하면 될듯??
# while True :
#     print('음식 추가 테스트')
#     input_name = input('메뉴 이름 입력: ')
#     input_cook_time = input('조리 시간 입력: ')
#     input_price = input('메뉴 가격 입력: ')

#     create_checker = test_menu_manager.create_menu(input_name, input_cook_time, input_price)
#     if create_checker == -1 :
#         recheck = input('다시 추가하시겠습니까? (Y/N): ')
#         if recheck == 'Y' :
#             continue
#         else :
#             break
#     elif create_checker == 0 :
#         print('정상적으로 메뉴가 추가되었습니다.')
#         test_menu_manager.print_menu()
#         break

main_menu = user_services.main_service_menu()
while True:
    main_menu.main_system()
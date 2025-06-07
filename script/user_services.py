'''
사용자가 시스템을 사용할 수 있도록 만드는 구조를 전부 저장.
메뉴 시스템을 보여주고, 각 선택지마다 함수를 호출
'''
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(current_dir, '..')
sys.path.append(main_dir)

from tabulate import tabulate
from core.menu import MenuManager
from core.order import OrderManager

class main_service_menu :
    def __init__(self, MenuManager, OrderManager):
        self.menu_manager = MenuManager
        self.order_manager = OrderManager
        pass

    def user_input_process(self, input_count, operator_mode_flag=False):
        '''
        사용자의 입력 처리 함수
        모든 서비스 선택 관련 입력은 여기서 진행하고, 오류 처리도 진행
        9999 입력시 관리자 메뉴로 돌입

        Input
        ; input_count - 입력의 갯수가 총 몇개인지
        ; operator_mode_flag - 관리자 메뉴를 접근하는 경우 확인, True면 9999 입력 가능
        Output
        ; 선택한 메뉴의 번호
        '''
        while True:
            user_input = input('메뉴를 선택해주세요: ')
            # Case 1. 입력이 정수가 아닌 경우
            try:
                int(user_input)
            except ValueError:
                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                continue
            
            # Case 2. 관리자 모드
            if operator_mode_flag == True and int(user_input) == 9999:
                return int(user_input)
            
            # Case 3. 입력이 주어진 범위를 벗어나는 경우
            if not (int(user_input) > 0 and int(user_input) <= input_count) :
                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                continue

            # Case 4. 정상 처리
            print()
            break
        return int(user_input)
        
    def main_system(self):
        '''
        일반 사용자가 접근하는 메인 시스템

        Input
        ; 없음
        Output
        ; 없음
        '''
        print('---------------- Main Menu ----------------')
        print('1 | Order Menu')
        print('-------------------------------------------')
        user_input = self.user_input_process(1, operator_mode_flag=True)
        if user_input == 1 :
            self.user_order_system()
        elif user_input == 9999 :
            print('관리자 메뉴로 진입합니다.\n')
            system_off = self.operator_system() # 시스템 종료시 False 반환
            if system_off == True :
                # 시스템 종료 돌입
                return False
        else :
            # 이 부분은 일반적으로는 접근 불가능해야함.
            print('Critical Error')
        return True

    def user_order_system(self) :
        '''
        사용자 주문 관련 시스템
        키오스크를 누르면 일단 메뉴가 쭉 뜨고, 메뉴 가격이 뜨고
        어떤 메뉴를 몇개
        현재 추가한 메뉴 출력해주고
        메뉴 수정 가능하게 해주고
        메뉴 삭제되게 해주고
        주문 완료 누르면
        최종 확인 해주고
        돌아갈 수 있게 해주고
        완료되면 달아주기

        Input
        ; 없음
        Output
        ; 없음
        '''
        menu_count = len(self.menu_manager.menu_items)
        # Corner case. 메뉴가 존재하지 않는 경우
        if menu_count == 0 :
            print('메뉴가 존재하지 않습니다. 관리자에게 문의해주세요.\n')
            return

        order_menu_list = []
        while True :
            self.menu_manager.print_menu_with_num_and_notime()
            user_input_name = input("주문할 메뉴를 선택해주세요: ")

            # 1. 입력이 정수인 경우
            try:
                int(user_input_name)
                # Corner Case. 입력이 잘못된 경우
                if int(user_input_name) <= 0 or int(user_input_name) > menu_count :
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
                selected_menu = list(self.menu_manager.menu_items.items())[int(user_input_name)-1]
            # 2. 입력이 문자인경우
            except ValueError : 
                # Corner Case. 입력이 잘못된 경우
                menu_object = self.menu_manager.menu_items.get(user_input_name) # get은 실패하면 None
                if menu_object is not None :
                    selected_menu = (user_input_name, menu_object)
                else :
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
            except IndexError :
                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                continue

            user_input_count = input("주문할 수량을 선택해주세요: ")
            try:
                int(user_input_count)
                if int(user_input_count) <= 0 :
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
            except ValueError :
                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                continue
            
            # 정상 처리
            print(f"{selected_menu[1].name} {int(user_input_count)}개 선택하셨습니다.")
            while True:
                user_input_checker = input("주문을 완료하시겠습니까? (Y/N): ")
                try:
                    if user_input_checker.lower() == "y" :
                        break
                    elif user_input_checker.lower() == "n" :
                        break
                    else :
                        print('잘못된 입력입니다. 다시 시도해주세요.\n')
                        continue
                except ValueError:
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
            
            print()
            if user_input_checker.lower() == "n" :
                continue
            
            # 주문 추가
            current_menu_item = selected_menu[1]
            current_menu_count = int(user_input_count)
            found_in_list = False
            # order_list를 순회하며 이미 해당 메뉴가 있는지 확인합니다.
            for order_item_dict in order_menu_list:
                # order_item_dict는 {MenuItem_object: count} 형태의 딕셔너리입니다.
                if current_menu_item in order_item_dict:
                    # 이미 메뉴가 존재하면 수량을 더합니다.
                    order_item_dict[current_menu_item] += current_menu_count
                    found_in_list = True
                    break  # 해당 메뉴를 찾았으므로 루프를 종료합니다.
            
            if not found_in_list:
                # 메뉴가 order_list에 없으면 새로 추가합니다.
                order_menu_list.append({current_menu_item: current_menu_count})

            # 현재까지 주문 리스트 출력
            self.print_order_list(order_menu_list)

            # 주문 계속 묻기
            while True:
                user_input_checker = input("주문을 계속하시겠습니까? (Y/N): ")
                try:
                    if user_input_checker.lower() == "y" :
                        break
                    elif user_input_checker.lower() == "n" :
                        break
                    else :
                        print('잘못된 입력입니다. 다시 시도해주세요.\n')
                        continue

                except ValueError:
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
            if user_input_checker.lower() == "n" :
                print()
                # 주문을 더 이상 안할 시
                # 결제 하고
                self.order_payment(order_menu_list)
                # 결제 완료되면 order 추가
                self.order_manager.create_order(order_menu_list)
                break
            else :
                print()
                continue
    
    def print_order_list(self, order_menu_list):
        '''
        order_list 리스트에 들어있는 주문 출력
        '''
        menu_num = 0
        headers = ["#", "Menu Name", "Amount", "Price"]
        table_data = []
        total_price = 0
        for order in order_menu_list :
            menu_num += 1
            menu_num_str = f"{menu_num:02d}"
            menu_object = list(order.keys())[0]
            menu_count = order[menu_object]
            price_str = f"{menu_object.price * menu_count:,} won"
            table_data.append([menu_num_str, menu_object.name, menu_count, price_str])
            total_price += menu_object.price * menu_count

        table_string = tabulate(table_data, headers=headers, tablefmt="orgtbl", colalign=("left", "left"))
        table_width = len(table_string.splitlines()[0])
        title_text = " Menu List "
        title_dash_length = table_width - len(title_text)
        formatted_title = f"{'-' * (int(title_dash_length / 2))}{title_text}{'-' * (int(title_dash_length / 2))}"        
        center_border = f"|{'-'*(table_width-2)}|"
        cell1_content = " Total Price: "
        cell2_content = f"{total_price:,} won"
        fixed_part_length = len("|") + len(cell1_content) + len("|")
        cell2_width = table_width - fixed_part_length
        footer_text = f"|{cell1_content}{cell2_content:<{cell2_width}}|"
        bottom_border = '-' * table_width
        
        print(formatted_title)
        print(table_string)
        print(center_border)
        print(footer_text)
        print(bottom_border)

    def order_payment(self, order_menu_list):
        '''
        간단한 계산 시스템
        '''
        total_price = 0
        for order in order_menu_list :
            menu_object = list(order.keys())[0]
            menu_count = order[menu_object]
            total_price += menu_object.price * menu_count
        print('--------------- Payment -------------------')
        print(f' Total Price: {total_price:,} won')
        print('-------------------------------------------')
        while True : # 계산 완료 loop
            user_pay_input = input("결제할 금액을 입력해주세요: ")
            try:
                if (int(user_pay_input) <= 0) :
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
            except ValueError: # 정수 입력이 아닐 시
                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                continue
                
            if int(user_pay_input) > total_price :
                print('게산이 완료되었습니다.')
                print(f'거스름돈: {int(user_pay_input) - total_price:,} 원\n')
                total_price = 0
            elif int(user_pay_input) == total_price :
                print('게산이 완료되었습니다.\n')
                total_price = 0
            else :
                print('금액이 부족합니다. 추가로 결제해주세요.')
                total_price -= int(user_pay_input)
                print(f'남은 금액: {total_price:,} 원\n')
            
            if total_price == 0 :
                break


#######################
### Operator System ###
#######################

    def operator_system(self) :
        '''
        관리자 전용 메뉴
        Input
        ; 없음
        Output
        ; True - Program off 메뉴 접근 시
        ; False - Previous Page 메뉴 접근 시
        '''
        while True :
            print('-------------- Operator Menu --------------')
            print('1 | Order Management')
            print('2 | Menu Management')
            print('3 | Tick Process')
            print('4 | Program Off')
            print('5 | Previous Page')
            print('-------------------------------------------')
            
            user_input = self.user_input_process(5)
            if user_input == 1 :
                self.order_system()
            elif user_input == 2 :
                self.menu_system()
            elif user_input == 3 :
                self.tick_system()
            elif user_input == 4 :
                self.end_system()
                return True
            elif user_input == 5 :
                return False
            else :
                # 이 부분은 일반적으로는 접근 불가능해야함.
                print('Critical Error')

    def order_system(self) :
        '''
        주문 관련 시스템
        1. 주문 생성
        2. 주문 확인
        3. 주문 수정 + 삭제
        4. 뒤로가기
        '''
        first_run_counter = True # 입력 잘못했을때 or 초기 실행시만 메뉴 목록 출력하게 만들기
        while True :
            if first_run_counter == True :
                print('---------------- Order Menu ---------------')
                print('1 | Create Order')
                print('2 | Print Order')
                print('3 | Update Order')
                print('4 | Delete Order')
                print('5 | Previous Page')
                print('-------------------------------------------')
                first_run_counter = False # False이면 While loop을 돌아도 위 메뉴가 출력 안됨
            
            user_input = self.user_input_process(5)
            if user_input == 1 :
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                self.user_order_system() # 일반적으로 관리자 모드에서 여기에 접근할 필요 없음

            elif user_input == 2 :
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                self.order_manager.print_order() # 우선은 모든 주문에 대한 정보 출력
                continue
                # 현재 Queue에 들어가있는 주문도 볼 수 있도록 추후 구현해야함

            elif user_input == 3 : # 주문 수정
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                order_count = len(self.order_manager.orders)
                # Corner Case. 주문이 없는 경우
                if order_count == 0 : 
                    print('주문이 존재하지 않습니다.\n')
                    continue
                
                while True :
                    self.order_manager.print_order_with_previous_page() # 주문이 존재하면, 일단 주문 목록 출력
                    update_input = input("수정할 주문을 선택하세요: ")
                    try :
                        int(update_input)
                        if update_input == '-1' : # 돌아가기 선택
                            print('이전 메뉴로 돌아갑니다.\n')
                            break
                        elif update_input <= '0' or int(update_input) > order_count : # 잘못된 범위
                            print('잘못된 입력입니다. 다시 시도해주세요.\n')
                            continue
                        else :
                            selected_order = self.order_manager.orders[int(update_input)-1]
                            self.order_manager.update_order(selected_order)
                    except ValueError :
                        print('잘못된 입력입니다. 다시 시도해주세요.\n')
                        continue
                

            elif user_input == 4 : # 주문 삭제
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기

            elif user_input == 5 :
                # 뒤로가기
                print('이전 메뉴로 돌아갑니다.\n')
                break
            else :
                # 일반적으로 접근 불가능
                print('Critical Error')
                break
        # Loop문 탈출하면 자동으로 돌아감
    
    def menu_system(self) :
        '''
        메뉴 관리 시스템
        관리자만 접근 가능해야 함 -> 구현할까?
        1. 메뉴 생성
        2. 메뉴 출력
        3. 메뉴 수정
        4. 메뉴 삭제
        5. 뒤로가기
        '''
        first_run_counter = True # 입력 잘못했을때 or 초기 실행시만 메뉴 목록 출력하게 만들기
        while True :
            if first_run_counter == True :
                print('------------- Menu Management -------------')
                print('1 | Create Menu')
                print('2 | Print Menu')
                print('3 | Update Menu')
                print('4 | Delete Menu')
                print('5 | Previous Page')
                print('-------------------------------------------')
                first_run_counter = False # False이면 While loop을 돌아도 위 메뉴가 출력 안됨
            
            user_input = self.user_input_process(5)
            if user_input == 1 : # 메뉴 추가
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                while True: # 메뉴 추가 루프
                    menu_count = len(self.menu_manager.menu_items)
                    if menu_count != 0 :
                        self.menu_manager.print_menu()
                    input_name = input('추가할 메뉴 이름 입력: ')
                    input_cook_time = input('추가할 조리 시간 입력: ')
                    input_price = input('추가할 메뉴 가격 입력: ')

                    create_checker = self.menu_manager.create_menu(input_name, input_cook_time, input_price)
                    if create_checker == -1 :
                        recheck = input('다시 추가하시겠습니까? (Y/N): ') # 입력에 실패한 경우, 다시 입력을 받을 지 여부
                        if recheck == 'Y' :
                            continue
                        else :
                            print('이전 메뉴로 돌아갑니다.\n')
                            break
                    elif create_checker == 0 :
                        print('정상적으로 메뉴가 추가되었습니다.\n')
                        break

            elif user_input == 2 : # 메뉴 출력
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                menu_count = len(self.menu_manager.menu_items)
                # Corner Case) 만약 메뉴가 없는 경우
                if menu_count == 0 :
                    print('메뉴가 존재하지 않습니다.\n')
                else :
                    self.menu_manager.print_menu()
            
            elif user_input == 3 : # 메뉴 수정
                # 일단 메뉴 리스트 출력
                # 수정할 메뉴 번호 or 이름 받기
                # 돌아가려면 -1? 아니면 돌아가기 번호를 밑에 추가
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                menu_count = len(self.menu_manager.menu_items)
                # Corner Case) 만약 메뉴가 없는 경우
                if menu_count == 0 :
                    print('메뉴가 존재하지 않습니다.\n')
                else :
                    self.menu_manager.print_menu_with_num()

                    while True : # 메뉴 수정 loop
                        update_input = input("수정할 메뉴를 선택하세요: ")
                        # 만약 입력이 숫자인 경우
                        try :
                            int(update_input)
                            if update_input == '-1' : # 돌아가기 선택
                                print('이전 메뉴로 돌아갑니다.\n')
                                break
                            elif update_input <= '0' or int(update_input) > menu_count : # 잘못된 범위
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue
                            else :
                                all_menu_keys = list(self.menu_manager.menu_items.keys())
                                original_key = all_menu_keys[int(update_input)-1]
                                menu_object = self.menu_manager.menu_items[original_key]
                                selected_menu = (original_key, menu_object)
                        except ValueError : # integer가 아님 -> 입력이 문자인 경우
                            menu_object = self.menu_manager.menu_items.get(update_input) # get은 실패하면 None
                            if menu_object is not None :
                                selected_menu = (update_input, menu_object)
                            else :
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue
                        except IndexError :
                            print('잘못된 입력입니다. 다시 시도해주세요.\n')
                            continue

                        # selected_menu를 수정하면 된다. 빈칸으로 두면 원래 것을 그대로 사용
                        original_key, menu_object_to_update = selected_menu
                        
                        print(f"선택한 메뉴 '{menu_object_to_update.name}' 의 정보를 수정합니다.")
                        print(f"빈칸을 입력하면 원래 값을 유지합니다.\n")
                        while True:
                            # 오류가 나면 다시 입력 받아야 함
                            input_name = input('변경할 메뉴 이름 입력: ')

                            # Error 1. 이미 존재하는 이름
                            if input_name in self.menu_manager.menu_items :
                                print(f'이미 존재하는 메뉴 이름입니다. 다시 입력해주세요.\n')
                                continue

                            # 빈칸인 경우 그대로 원래 이름 사용
                            if input_name == '' :
                                input_name = menu_object_to_update.name

                            input_cook_time = input('변경할 조리 시간 입력: ')
                            try:
                                if input_cook_time == '' : # 빈칸인 경우 그대로 사용
                                    input_cook_time = menu_object_to_update.cook_time
                                else :
                                    int(input_cook_time)
                            except ValueError:
                                # Error 1. 정수가 아님
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue
                            if int(input_cook_time) < 0 :
                                # Error 2. 음수
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue

                            input_price = input('변경할 메뉴 가격 입력: ')
                            try:
                                if input_price == '' : # 빈칸인 경우 그대로 사용
                                    input_price = menu_object_to_update.price
                                else :
                                    int(input_price)
                            except ValueError:
                                # Error 1. 정수가 아님
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue
                            if int(input_price) < 0 :
                                # Error 2. 음수
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue

                            # 정상 처리
                            self.menu_manager.update_menu(original_key, input_name, int(input_cook_time), int(input_price))
                            print('정상적으로 수정되었습니다.\n')
                            break
                        break
            
            elif user_input == 4 : # 메뉴 삭제
                first_run_counter = True # 메뉴가 정상적으로 선택되면 위 메뉴가 출력되도록 만들기
                menu_count = len(self.menu_manager.menu_items)
                # 만약 메뉴가 없는 경우
                if menu_count == 0 :
                    print('메뉴가 존재하지 않습니다. \n')
                else :
                    self.menu_manager.print_menu_with_num()

                    while True : # 메뉴 삭제 loop
                        delete_input = input("삭제할 메뉴를 선택하세요: ")
                        # 만약 입력이 숫자인 경우
                        try :
                            int(delete_input)
                            if delete_input == '-1' : # 돌아가기
                                print('이전 메뉴로 돌아갑니다.\n')
                                break
                            elif delete_input <= '0' or int(delete_input) > menu_count : # 잘못된 입력
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue
                            else : # 정상 입력
                                all_menu_keys = list(self.menu_manager.menu_items.keys())
                                original_key = all_menu_keys[int(delete_input)-1]
                                menu_object = self.menu_manager.menu_items[original_key]
                                selected_menu = (original_key, menu_object)
                        except ValueError : # integer가 아닌 경우
                            menu_object = self.menu_manager.menu_items.get(delete_input) # get은 실패하면 None
                            if menu_object is not None :
                                selected_menu = (delete_input, menu_object)
                            else :
                                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                                continue

                        original_key, menu_object_to_delete = selected_menu
                        self.menu_manager.delete_menu(original_key)
                        print('정상적으로 삭제되었습니다.\n')
                        break

            elif user_input == 5 : 
                print('이전 메뉴로 돌아갑니다.\n')
                break
            else :
                # 일반적으로 접근 불가능
                print('Critical Error')
                break
        # Loop문 탈출하면 자동으로 돌아감
    
    def tick_system(self) :
        pass

    def end_system(self) :
        '''
        프로그램 종료, 현재 남아있는 데이터와 메뉴를 저장하고 end 해야함
        '''
        print('프로그램을 종료합니다.')
        pass
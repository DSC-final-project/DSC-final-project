'''
사용자가 시스템을 사용할 수 있도록 만드는 구조를 전부 저장.
메뉴 시스템을 보여주고, 각 선택지마다 함수를 호출
'''
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
main_dir = os.path.join(current_dir, '..')
sys.path.append(main_dir)

from core.menu import MenuManager

class main_service_menu :
    def __init__(self, MenuManager):
        self.menu_manager = MenuManager
        pass

    def user_input_process(self, input_count):
        '''
        사용자의 입력 처리 함수
        모든 서비스 선택 관련 입력은 여기서 진행하고, 오류 처리도 진행

        Input
        ; input_count - 입력의 갯수가 총 몇개인지
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

            # Case 2. 입력이 주어진 범위를 벗어나는 경우
            if not (int(user_input) > 0 and int(user_input) <= input_count) :
                print('잘못된 입력입니다. 다시 시도해주세요.\n')
                continue

            # Case 3. 정상 처리
            print()
            break
        return int(user_input)
    
    def user_input_process_with_hidden_menu(self, input_count):
        '''
        사용자의 입력 처리 함수
        여기에 hidden menu 선택지 잇음
        9999 입력시 관리자 메뉴로 돌입

        Input
        ; input_count - 입력의 갯수가 총 몇개인지
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

            # Case 2. 입력이 주어진 범위를 벗어나는 경우
            if not (int(user_input) > 0 and int(user_input) <= input_count) :
                if not int(user_input) == 9999 :
                    print('잘못된 입력입니다. 다시 시도해주세요.\n')
                    continue
            
            # Case 3. 정상 처리
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
        user_input = self.user_input_process_with_hidden_menu(1)
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

    def operator_system(self) :
        '''
        관리자 전용 메뉴
        Input
        ; 없음
        Output
        ; True - Program off 메뉴 접근 시
        ; False - Previous Page 메뉴 접근 시
        '''
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
        return False

    def user_order_system(self) :
        '''
        사용자 주문 관련 시스템
        '''
        print('hi')
        pass

    def order_system(self) :
        '''
        주문 관련 시스템
        1. 주문 생성
        2. 주문 확인
        3. 주문 수정 + 삭제
        4. 뒤로가기
        '''
        print('---------------- Order Menu ---------------')
        print('1 | Make Order')
        print('2 | Check Order')
        print('3 | Modify Order')
        print('4 | Previous Page')
        print('-------------------------------------------')
        while True :
            user_input = self.user_input_process(4)
            if user_input == 1 :
                pass
            elif user_input == 2 :
                pass
            elif user_input == 3 :
                pass
            elif user_input == 4 :
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
                    input_name = input('메뉴 이름 입력: ')
                    input_cook_time = input('조리 시간 입력: ')
                    input_price = input('메뉴 가격 입력: ')

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
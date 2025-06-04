'''
사용자가 시스템을 사용할 수 있도록 만드는 구조를 전부 저장.
메뉴 시스템을 보여주고, 각 선택지마다 함수를 호출
'''
from core.menu import MenuManager

class main_service_menu :
    def __init__(self):
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
        
    def main_system(self):
        '''
        메인 시스템
        이 함수를 호출할 때 True 조건을 걸어두고,
        End system을 선택한 경우 False를 반환하게 함

        1. 주문 관리
        2. 메뉴 관리
        3. 틱 진행
        4. 종료

        Input
        ; 없음
        Output
        ; 일반적인 경우 True 반환
        ; End_system이 호출된 경우 False를 반환 -> 종료
        '''
        print('---------------- Main Menu ----------------')
        print('1 | Order Management')
        print('2 | Menu Management')
        print('3 | Tick Process')
        print('4 | Program Off')
        print('-------------------------------------------')
        user_input = self.user_input_process(4)
        if user_input == 1 :
            self.order_system()
        elif user_input == 2 :
            self.menu_system()
        elif user_input == 3 :
            self.tick_system()
        elif user_input == 4 :
            self.end_system()
            return False
        else :
            # 이 부분은 일반적으로는 접근 불가능해야함.
            print('Critical Error')
        return True
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
        pass
    
    def menu_system(self) :
        '''
        메뉴 관리 시스템
        관리자만 접근 가능해야 함 -> 구현할까?
        1. 메뉴 생성
        2. 메뉴 출력
        3. 메뉴 수정 + 삭제
        4. 뒤로가기
        '''
        print('------------- Menu Management -------------')
        print('1 | Create Menu')
        print('2 | Print Menu')
        print('3 | Modify Menu')
        print('4 | Previous Page')
        print('-------------------------------------------')
        pass
    
    def tick_system(self) :
        pass

    def end_system(self) :
        '''
        프로그램 종료, 현재 남아있는 데이터와 메뉴를 저장하고 end 해야함

        '''
        print('프로그램을 종료합니다.')
        pass
class MenuItem:
    def __init__(self, name, cook_time, price):
        self.name = name
        self.cook_time = cook_time  # in minutes
        self.price = price

'''
이미 주문이 들어간 메뉴의 정보를 update or delete하면 어떻게 Handle?
-> 주문이 들어간 애는 수정이 불가능하게 설정
'''

class MenuManager:
    def __init__(self):
        '''
        하드코딩을 기반으로, 시스템에서 업데이트하면 여기서도 추가
        '''
        self.menu_items = {
            "Americano": MenuItem("Americano", 3, 3000),
            "Latte": MenuItem("Latte", 5, 3500),
            "Mocha": MenuItem("Mocha", 6, 3800),
            "Espresso": MenuItem("Espresso", 2, 2500)
        }

    def get_menu(self):
        return self.menu_items
    
    def check_menu_already_on_queue(self, menu_name) :
        '''
        CRUD 기능에서, 해당 메뉴가 Queue에 이미 존재하는 지 체크
        이 함수에 들어오는 menu_name은 유효성 검사 완료

        Input
        ; menu_name - 검사할 메뉴 이름
        Output
        ; True - 이미 존재하는 경우
        ; False - 존재하지 않는 경우
        '''
        pass

    def create_menu(self, menu_name, menu_cook_time, menu_price):
        '''
        메뉴 추가, 이름, 가격, 조리시간 추가
        이미 존재하는 메뉴를 추가하려 할 시 Error -> update할지, 취소시킬지 ?

        Input
        ; menu_name - 추가할 메뉴 이름
        ; menu_cook_time - 추가할 메뉴의 조리 시간
        ; menu_price - 추가할 메뉴 가격
        Output
        ; return 0  - 정상 추가
        ; return -1 - Error Case
        '''

        # Case 1. 메뉴 이름이 string이 아니거나 비어있는 경우
        if not isinstance(menu_name, str) or menu_name == '' :
            print(f'Error: 메뉴 이름이 올바르지 않습니다. '
                  f'현재 입력 받은 값은 다음과 같습니다.')
            print(f'       메뉴 이름: {menu_name}, 조리 시간: {menu_cook_time} min, 메뉴 가격: {menu_price} won')
            print()
            return -1

        # Case 2. 이미 해당 메뉴가 존재하는 경우
        if menu_name in self.menu_items :
            print(f'Error: 이미 존재하는 메뉴 이름입니다. '
                  f'현재 입력 받은 값은 다음과 같습니다.')
            print(f'       메뉴 이름: {menu_name}, 조리 시간: {menu_cook_time} min, 메뉴 가격: {menu_price} won')
            print()
            return -1
        
        # Case 3. 메뉴 조리 시간, 메뉴 가격이 정수가 아닌 경우
        try:
            menu_cook_time_integer = int(menu_cook_time)
            menu_price_integer = int(menu_price)
        except ValueError:
            print(f'Error: 입력 값이 정수가 아닙니다. '
                  f'현재 입력 받은 값은 다음과 같습니다.')
            print(f'       메뉴 이름: {menu_name}, 조리 시간: {menu_cook_time} min, 메뉴 가격: {menu_price} won')
            print()
            return -1

        # Case 4. 메뉴 조리 시간, 메뉴 가격이 음수인 경우
        if (menu_cook_time_integer < 0 or menu_price_integer < 0) :
            print(f'Error: 입력 값이 음수입니다.'
                  f'현재 입력 받은 값은 다음과 같습니다. ')
            print(f'       메뉴 이름: {menu_name}, 조리 시간: {menu_cook_time_integer} min, 메뉴 가격: {menu_price_integer} won')
            print()
            return -1

        # 정상 처리
        self.menu_items[menu_name] = MenuItem(menu_name, menu_cook_time_integer, menu_price_integer)
        return 0

    def update_menu(self):
        '''
        메뉴 업데이트, 이미 존재하는 메뉴를 리스트로 나열하고, 선택해서 업데이트
        '''
        pass

    def delete_menu(self, menu_name):
        '''
        메뉴 삭제, 입력 받은 메뉴를 삭제함
        
        메뉴 삭제, 이미 존재하는 메뉴를 리스트로 나열하고, 선택해서 삭제
        '''

        pass

    def print_menu(self):
        '''
        메뉴 목록 리스트로 출력
        Formatting 맞춰놨는데, 나중에 외부 라이브러리로 예쁘게 만드는 것도 고려해봐야할듯
        '''
        print('---------------- Menu List ----------------')
        print('Menu Name            | Cook Time | Price')
        for menu, dict in self.menu_items.items() :
            print(f"{dict.name:20s} | {dict.cook_time:02d} min    | {dict.price:d} won")
        print('-------------------------------------------')
        print()
        pass
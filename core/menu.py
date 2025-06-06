from tabulate import tabulate # 예쁜 출력을 위해

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
            "아메리카노": MenuItem("아메리카노", 3, 3000),
            "카페라떼": MenuItem("카페라떼", 5, 3500),
            "카페모카": MenuItem("카페모카", 6, 3800),
            "에스프레소": MenuItem("에스프레소", 2, 2500),
            "카푸치노":MenuItem("카푸치노", 5, 4000),
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

    def update_menu(self, original_key, new_name, new_cook_time, new_price):
        '''
        메뉴 업데이트, 이미 존재하는 메뉴를 리스트로 나열하고, 선택해서 업데이트

        Input 
        ; original_key - 원본 키
        ; new_name - 업데이트할 이름
        ; new_cook_time - 업데이트할 조리 시간
        ; new_price - 업데이트할 가격
        Output
        ; 없음
        '''
        # 1. 원본 키를 사용해 수정할 메뉴 객체를 가져옵니다.
        menu_object_to_update = self.menu_items[original_key]

        # 2. 객체의 속성을 새로운 값으로 업데이트합니다.
        menu_object_to_update.name = new_name
        menu_object_to_update.cook_time = new_cook_time
        menu_object_to_update.price = new_price

        # 3. 메뉴 이름(딕셔너리의 키)이 변경되었다면,
        if new_name != original_key:
            # 새로운 이름으로 딕셔너리에 항목을 추가하고,
            self.menu_items[new_name] = menu_object_to_update
            # 이전 키를 가진 항목을 삭제합니다.
            del self.menu_items[original_key]

    def delete_menu(self, original_key):
        '''
        메뉴 삭제, 입력 받은 메뉴를 삭제함
        Input
        ; original_key - 삭제할 메뉴의 키
        Output
        ; 없음
        '''
        del self.menu_items[original_key]

    def print_menu(self):
        '''
        메뉴 목록 리스트로 출력
        Tabulate 라이브러리로 출력 예쁘게 만듦
        '''
        headers = ["Menu Name", "Cook Time", "Price"]
        table_data = []
        for menu, dict in self.menu_items.items() :
            cook_time_str = f"{dict.cook_time:02d} min"
            price_str = f"{dict.price:,} won"
            table_data.append([dict.name, cook_time_str, price_str])
        
        table_string = tabulate(table_data, headers=headers, tablefmt="orgtbl", colalign=("left", "left", "left"))
        table_width = len(table_string.splitlines()[0])
        title_text = " Menu List "
        title_dash_length = table_width - len(title_text)
        formatted_title = f"{'-' * (int(title_dash_length / 2))}{title_text}{'-' * (int(title_dash_length / 2))}"
        bottom_border = "-" * table_width

        print(formatted_title)
        print(table_string)
        print(bottom_border)
        print()

    def print_menu_with_num(self):
        '''
        메뉴 목록을 리스트로 출력하면서, 번호도 매겨줌
        -1로 돌아가기도 출력
        끝에 print() 안함
        '''
        menu_num = 0
        headers = ["#", "Menu Name", "Cook Time", "Price"]
        table_data = []
        for menu, dict in self.menu_items.items() :
            menu_num += 1
            menu_num_str = f"{menu_num:02d}"
            cook_time_str = f"{dict.cook_time:02d} min"
            price_str = f"{dict.price:,} won"
            table_data.append([menu_num_str, dict.name, cook_time_str, price_str])
        
        table_string = tabulate(table_data, headers=headers, tablefmt="orgtbl", colalign=("left", "left", "left"))
        table_width = len(table_string.splitlines()[0])
        title_text = " Menu List "
        title_dash_length = table_width - len(title_text)
        formatted_title = f"{'-' * (int(title_dash_length / 2))}{title_text}{'-' * (int(title_dash_length / 2))}"        
        bottom_middle_border = f"|{'-'*(table_width-2)}|"
        bottom_border = "-" * table_width
        cell1_content = " -1  "
        cell2_content = " Prevous Page"
        fixed_part_length = len("|") + len(cell1_content) + len("|") + len("|")
        cell2_width = table_width - fixed_part_length
        footer_text = f"|{cell1_content}|{cell2_content:<{cell2_width}}|"

        print(formatted_title)
        print(table_string)
        print(bottom_middle_border)
        print(footer_text)
        print(bottom_border)
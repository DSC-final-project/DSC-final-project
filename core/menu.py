class MenuItem:
    def __init__(self, name, cook_time, price):
        self.name = name
        self.cook_time = cook_time  # in minutes
        self.price = price

'''
문제점: 이미 주문이 들어간 메뉴의 정보를 update or delete하면 어떻게 Handle?
1. 주문이 들어간 애는 수정이 불가능하게 설정
2. 들어간 주문에는 수정 전 데이터를 달아주기 -> 추가로 무언가 설정 필요
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
    
    def create_menu(self):
        '''
        메뉴 추가, 이름, 가격, 조리시간 추가
        이미 존재하는 메뉴를 추가하려 할 시 Error -> update할지, 취소시킬지 ?
        '''
        pass

    def update_menu(self):
        '''
        메뉴 업데이트, 이미 존재하는 메뉴를 리스트로 나열하고, 선택해서 업데이트
        '''
        pass

    def delete_menu(self):
        '''
        메뉴 삭제, 이미 존재하는 메뉴를 리스트로 나열하고, 선택해서 삭제
        '''
        pass

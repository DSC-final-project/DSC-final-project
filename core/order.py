from structures.heap import PriorityQueue
from structures.queue import Queue
from tabulate import tabulate, SEPARATING_LINE
from core.menu import MenuItem # MenuManager는 OrderManager 생성자에서만 필요하므로 여기서 제거

class Order:
    def __init__(self, order_id: int, order_time: int = None): # menu 파라미터 제거, order_time 기본값 None
        '''
        메뉴를 order에 묶어만 놓고, 개별적으로 priority queue에 넣으면서 관리 예정
        주문이 들어오면 Queue에는 동일 주문 기준 시간이 가장 오래걸리는 것부터 정렬하여 동시에 넣기
        이를 통해 Priority queue에 들어가는 애들을 긴것 부터 넣어서 최대한 대기 시간이 짧도록 관리 가능

        order_id - 주문 번호
        order_time - 주문 시점
        start_time - 메뉴 별 조리 시작 시점
        menu_list - 메뉴 목록
        estimanted_finish_time - 메뉴 별 예상 완료 시점
        '''
        self.order_id = order_id
        self.order_time = order_time
        self.menu_list = [] # MenuItem 객체들이 저장될 리스트
        self.start_time = None # 우선 None으로 초기화
        self.estimated_finish_time = None

class OrderManager:
    def __init__(self, MenuManager, capacity=20):
        self.menu_manager = MenuManager
        # self.priority_queue = PriorityQueue(capacity)
        # self.waiting_queue = Queue()
        self.order_counter = 1
        self.orders = {}

    def create_order(self, order_menu_list):
        '''
        입력받은 주문의 목록을 Order라는 객체에 담기
        메뉴 목록을 나누고, 조리 시간을 기준으로 내림차순 정렬하고,
        메뉴 리스트를 생성하여 관리

        Input
        ; order_menu_list - [{MenuItem_object: count}, {MenuItem_object: count}, ...]
        '''
        current_order_id = self.order_counter
        # order_time은 현재 시점에서는 사용하지 않으므로 None 또는 특정 값으로 설정 가능
        # 여기서는 Order 객체의 기본값을 사용하도록 order_time을 전달하지 않거나 None으로 전달합니다.
        new_order = Order(order_id=current_order_id)

        temp_menu_list_for_sorting = []
        for item_dict in order_menu_list:
            for menu_item, count in item_dict.items():
                for _ in range(count):
                    temp_menu_list_for_sorting.append(menu_item)
        
        # cook_time을 기준으로 내림차순 정렬
        # MenuItem 객체에 __lt__ 또는 __gt__가 정의되어 있지 않다면 lambda 사용 필요
        # MenuItem 클래스에 cook_time 속성이 있다고 가정합니다.
        temp_menu_list_for_sorting.sort(key=lambda item: item.cook_time, reverse=True)
        
        new_order.menu_list = temp_menu_list_for_sorting
        # start_time과 estimated_finish_time은 추후 구현 시 설정

        self.orders[current_order_id] = new_order
        self.order_counter += 1

    def update_order(self, order_id, new_menu_name) -> bool :
        # 구현: 기존 큐에서 제거 후 재삽입
        # if queue안에 있으면 바꾸고 return true
        # else 이미 heap으로 들어갔으면 return false
        pass

    def delete_order(self, order_id):
        # 구현: 큐에서 제거 및 재정렬
        pass

    def print_order(self):
        '''
        현재 시스템에 저장된 모든 주문 목록을 출력합니다.
        각 주문의 ID와 해당 주문에 포함된 메뉴 목록을 tabulate를 사용하여 표시합니다.
        '''
        if not self.orders:
            print("현재 주문 내역이 없습니다.\n")
            return
    
        headers = ["Order ID", "Menu Item", "Cook Time"]
        colalign = ("right", "left", "left")
        tablefmt = "orgtbl"
    
        # 헤더를 기반으로 테이블 전체 너비 계산
        # tabulate 라이브러리가 빈 데이터([])와 colalign을 함께 사용할 때 IndexError가 발생할 수 있으므로,
        # 헤더와 동일한 수의 컬럼을 가진 더미 행을 제공하여 문제를 회피합니다.
        dummy_row_for_width_calc = [[""] * len(headers)]
        header_table_string_for_width = tabulate(dummy_row_for_width_calc, headers=headers, tablefmt=tablefmt, colalign=colalign)
        if not header_table_string_for_width.splitlines():
            print("주문 목록을 표시하는 중 오류가 발생했습니다. (너비 계산 불가)\n")
            return
        max_table_width = len(header_table_string_for_width.splitlines()[0])
    
        # 사용자 정의 구분선 (center_border 스타일)
        # 다른 print 함수들과의 일관성을 위해 `|`로 감싸고 내부를 `-`로 채웁니다.
        # 순수 대시 라인을 원하시면: custom_separator_line = "-" * max_table_width
        custom_separator_line = f"|{'-' * (max_table_width - 2)}|"
    
        # 테이블 제목 출력
        title_text = " Order List "
        title_dash_length = max(0, max_table_width - len(title_text))
        left_dashes = title_dash_length // 2
        right_dashes = title_dash_length - left_dashes
        formatted_title = f"{'-' * left_dashes}{title_text}{'-' * right_dashes}"
        print(f"\n{formatted_title}")
    
        # 헤더 출력 (tabulate를 사용하여 orgtbl의 헤더 스타일 적용)
        header_lines = header_table_string_for_width.splitlines()
        print(header_lines[0]) # 헤더 텍스트 라인
        print(header_lines[1]) # 헤더 구분선 라인 (|---+---+---|)
    
        sorted_order_ids = sorted(self.orders.keys())
    
        for i, order_id in enumerate(sorted_order_ids):
            order_obj = self.orders[order_id]
            current_order_data_rows = []
    
            if not order_obj.menu_list:
                # order_id를 문자열로 변환
                current_order_data_rows.append([str(order_obj.order_id), "주문된 메뉴 없음", ""])
            else:
                for item_idx, menu_item_obj in enumerate(order_obj.menu_list):
                    # order_id를 문자열로 변환
                    order_id_to_display = str(order_obj.order_id) if item_idx == 0 else ""
                    # menu_item_obj가 MenuItem 인스턴스이고 필요한 속성을 가지고 있는지 확인 (방어적 코딩)
                    menu_name = getattr(menu_item_obj, 'name', '알 수 없는 메뉴') # 속성이 없으면 '알 수 없는 메뉴' 반환
                    cook_time = getattr(menu_item_obj, 'cook_time', 0) # 속성이 없으면 0 반환
                    cook_time_str = f"{cook_time} min"
                    current_order_data_rows.append([order_id_to_display, menu_name, cook_time_str])
    
            if current_order_data_rows:
                # 현재 주문의 데이터 행들만 tabulate로 포맷팅 (헤더 없이)
                # orgtbl 포맷으로 각 주문 데이터를 포맷팅하되, 실제 출력은 데이터 라인만 가져옴
                # 컬럼 너비 일관성을 위해 headers를 전달하여 tabulate가 너비를 맞추도록 유도
                order_block_table_str = tabulate(current_order_data_rows, headers=headers, tablefmt=tablefmt, colalign=colalign)
                order_block_lines = order_block_table_str.splitlines()
                for line_idx in range(2, len(order_block_lines)): # 각 블록의 헤더와 그 구분선은 제외하고 데이터 라인만 출력
                    print(order_block_lines[line_idx])
    
            # 마지막 주문이 아닐 경우 사용자 정의 구분선 추가
            if i < len(sorted_order_ids) - 1:
                print(custom_separator_line)
    
        # 전체 테이블의 하단 테두리
        bottom_border = "-" * max_table_width
        print(bottom_border)
        print()
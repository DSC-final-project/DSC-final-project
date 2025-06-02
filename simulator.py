class TimeStepper:
    def __init__(self, order_manager):
        self.time = 0
        self.order_manager = order_manager

    def step(self):
        self.time += 1
        # 완료된 주문 제거
        # 큐 이동 및 정렬 갱신
        # print current state if needed

class Menu:
    def __init__(self, name: str, cook_time: int, price: int):
        self.name = name
        self.cook_time = cook_time
        self.price = price


class MenuManager:
    def __init__(self):
        self.menu_items = {}

    def create_menu(self, name, time, price):
        self.menu_items[name] = Menu(name, time, price)

    def update_menu(self, name, time=None, price=None):
        if name in self.menu_items:
            if time is not None:
                self.menu_items[name].cook_time = time
            if price is not None:
                self.menu_items[name].price = price

    def delete_menu(self, name):
        self.menu_items.pop(name, None)

    def list_menu(self):
        return list(self.menu_items.values())

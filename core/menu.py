class MenuItem:
    def __init__(self, name, cook_time, price):
        self.name = name
        self.cook_time = cook_time  # in minutes
        self.price = price

class MenuManager:
    def __init__(self):
        self.menu_items = {
            "Americano": MenuItem("Americano", 3, 3000),
            "Latte": MenuItem("Latte", 5, 3500),
            "Mocha": MenuItem("Mocha", 6, 3800),
            "Espresso": MenuItem("Espresso", 2, 2500)
        }

    def get_menu(self):
        return self.menu_items

#hello

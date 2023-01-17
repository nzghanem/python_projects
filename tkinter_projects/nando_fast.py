from tinydb import TinyDB, Query
import collections

db = TinyDB('nando_fast.json')


class Food_Items:
    def __init__(self, ids, names, prices):
        Food_Items = collections.namedtuple('Food_Items', (ids, names, prices))


class Menu:
    def __init__(self):
        self.food_info = self.get_info()
        print("step 1")

    def get_info(self):
        names = ["French fries", "1/4 pound burger", "1/4 pound cheeseburger",
                 "1/2 pound burger", "1/2 pound cheeseburger", "medium pizza",
                 "medium pizza with extra toppings",
                 "large pizza", "large pizza with extra toppings", "Garlic bread"]
        prices = [2, 5, 5.5, 7, 7.5, 9, 11, 12, 14.5, 4.5]
        ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        d = dict(zip(ids, zip(names, prices)))
        db.insert({"food_items": d})
        return d


menu = Menu()


class Orders:

    def __init__(self):
        self.main_menu = self.main_menu()
        print("step 2 ")
        self.order_info = self.get_order()
        print("step 3")
        self.display_object = self.display_info()
        print("step 4")

    def main_menu(self):
        print("-" * 10 + "MAIN MENU" + "-" * 10 + "\n"
              "(O) Order\n" "(P) Payment\n" "(E) Exit\n" + "-" * 30)

        customer_1 = str(input("Please Select Your Operation: "))
        while True:
            if (customer_1 == 'O' or customer_1 == 'o'):
                print("-"*70)
                for k, v in menu.food_info.items():
                    print(k, ":", v[0], "for $", v[1])
                print("-"*70)
                break
            elif (customer_1 == 'P'):
                print("Feature not available yet!")
                print("Sorry 😭\n"*20)
                exit()
            elif (customer_1 == 'E'):
                print("🤡" * 10 + "THANK YOU" + "🤡" * 10 + "\n")
                exit()
            else:
                print("ERROR (" + str(customer_1) + "). Try again!")
                exit()

    def get_order(self):

        food = []
        price = []
        quantity = []

        while True:
            input_1 = int(input("Please Select Your Order. Chosse a Number!\n"))
            quantity_customer = int(input("How many do you want?\n"))
            for k, v in menu.food_info.items():
                if k == input_1:
                    food.append(v[0])
                    price.append(v[1])
                    quantity.append(quantity_customer)
            x = True
            while x == True:
                input_n = str(input("Anything else! Yes or No\n"))
                if input_n == "Yes" or input_n in "Yy":
                    input_1 = int(input("Please Select Your Order. Chosse a Number!\n"))
                    quantity_customer = int(input("How many do you want?\n"))
                    for k, v in menu.food_info.items():
                        if k == input_1:
                            food.append(v[0])
                            price.append(v[1])
                            quantity.append(quantity_customer)
                            x = True

                elif input_n == "No" or input_n in "Nn":
                    print("Thank you for ordering with us ")
                    x = False

                else:
                    print("Fatal mistake, program stopping and here is your current order. 🤯\n")
                    x = False
            d = dict(zip(food, zip(price, quantity)))
            db.insert({"Customer Order": d})
            return d

    def display_info(self):
        print("🍟"*50, "\n")
        total_cost = 0
        for k, v in self.order_info.items():
            total_meal_cost = v[1]*v[0]
            print("|", k, "for $", v[0], "ordered quantity is", v[1],
                  "and the total cost for this meal is $", total_meal_cost,  "|")
            total_cost += total_meal_cost
        print("**", "The total cost of the order is $", total_cost, "**", "\n")
        print("🍕"*50, "\n")
        db.insert({"Total payment made by the customer": total_cost})
        return total_cost


order = Orders()


class Calculations:

    def __init__(self):
        self.generate_more_orders = self.more_orders()
        print("step 5")
        self.finance = self.profits_revenue()
        print("You are done for today 🤗\n"*5)

    def more_orders(self):
        total_revenue = []
        total_revenue.append(order.display_object)
        x = True
        while x == True:
            input_n = input("Is the day over? Yes or No\n")
            if input_n == "No" or input_n in "Nn":
                new_order = Orders()
                total_revenue.append(new_order.display_object)
                x = True

            elif input_n == "Yes" or input_n in "Yy":
                print("👏It was a great profitable day👏")
                x = False

            else:
                print("Fatal mistake, program stopping and here is your current order. 👾👾👾👾\n")
                x = False
        return total_revenue

    def profits_revenue(self):
        total_revenue = sum(self.generate_more_orders)
        percentage = float(input(
            "What is the percentage of daily taking that are profit? \nPlease use only decimals .e.g. 0.3, 0.9\n"))
        profit = total_revenue*percentage
        print("The total daily takings is $", total_revenue)
        print("The profit for the day is", profit)
        print("The percentage of profit used is %", percentage*100)
        db.insert({total_revenue: profit})


calculations = Calculations()

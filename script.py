from pakages import *

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# --------------------------------------------------------- #
def print_color(string, color: str="r"):
    if color == "r":
        print(Fore.RED + f"\n{string}\n" + Fore.RESET)

    elif color == "b":
        print(Fore.BLUE + f"\n{string}\n" + Fore.RESET)
    
    elif color == "g":
        print(Fore.GREEN + f"\n{string}\n" + Fore.RESET)
    
    elif color == "m":
        print(Fore.MAGENTA + f"\n{string}\n" + Fore.RESET)

    elif color == "y":
        print(Fore.YELLOW + f"\n{string}\n" + Fore.RESET)
    
    elif color == "c":
        print(Fore.CYAN + f"\n{string}\n" + Fore.RESET)
    
    else:
        print (f"\n{string}\n")

# --------------------------------------------------------- #

class ReadWriteData:

    @staticmethod
    def get_path(path_type: str) -> str:

        """path file is file of path"""

        if path_type == "user":
            return "./json/User.json"
        
        elif path_type == "car":
            return "./json/Car.json"
        
        elif path_type == "deal":
            return "./json/CarDealingList.json"
        
        else:
            return "./json/Unknown.json"

# -------------------- #

    @staticmethod
    def read(path_type: str) -> dict:

        """path_type is a path of file reading."""

        path = ReadWriteData.get_path(path_type)

        if not os.path.exists(path):
            return {}
        
        else:
            with open(path) as F:
                return json.load(F)
            
# -------------------- #
    
    @staticmethod
    def write(data: dict, path_type: str) -> None:
        """path_type is path of file writing."""
        path = ReadWriteData.get_path(path_type)
        with open(path, "w") as F:
            json.dump(data, F, indent=4)
        
# --------------------------------------------------------- #

class CarDealingList:

    @staticmethod
    def read_dealings(path: str="deal"):
        data = ReadWriteData.read(path)

        return data
    
# -------------------- #

    @staticmethod
    def write_dealings(data, path: str= "deal"):
        ReadWriteData.write(data, path)

# --------------------------------------------------------- #

class Car:

    car_color = set()
    car_brand = set()

    def __init__(self, car_id):
        self.car_id = car_id
        self.all_cars = Car.read_car()
        self.car_info = self.all_cars[car_id]

        self.car_brand = self.car_info["brand"]
        self.car_model = self.car_info["model"]
        self.car_year = self.car_info["year"]
        self.car_color = self.car_info["color"]
        self.car_km = self.car_info["km"]
        self.car_plate = self.car_info["plate"]
        self.car_sell_price = self.car_info["sell_price"]
        self.car_buy_price = self.car_info["buy_price"]
        self.quantity = self.car_info["quantity"]

# -------------------- #

    def edit_car(self):

        data = Car.read_car()

        admin = Admin("mhghasri")

        old_amount = self.car_buy_price * self.quantity
        
        brand = input("\nEnter brand of car: ")
        model = input("\nEnter model of car: ")
        year = input("\nEnter year of car: ")
        color = input("\nEnter color of car: ")
        km = input("\nEnter km of car: ")
        plate = input("\nEnter plate of car: ")
        quantity = int(input("\nEnter quantity of car: "))
        buy_price = int(input("\nEnter buy price of car: "))
        sell_price = buy_price * 1.3

        data[self.car_id] = {
            "brand" : brand.title(),
            "model" : model,
            "year" : year,
            "color" : color,
            "km" : km,
            "plate" : plate,
            "quantity" : quantity,
            "buy_price" : buy_price,
            "sell_price" : sell_price
        }

        current_amount = quantity * buy_price


        new_amount = current_amount - old_amount



        if admin.balance >= new_amount:

            Car.write_car(data)

            admin.change_balance(amount= new_amount, mode="admin_buy")

            print_color("Car edited successfully.", "g")

            


        else:

            print_color(f"not enough money. current money is '{admin.balance}$'")

            return False

# -------------------- #

    @classmethod
    def sort_car_color(cls):
        data = cls.read_car()


        car_data_color = []
            
        for car in data.values():
            car_data_color.append(car["color"])

        for color in car_data_color:
            cls.car_color.add(color)

        return cls
    
# -------------------- #

    @classmethod
    def sort_car_by_color(cls):
        cls.sort_car_color()
        car_data = cls.read_car()
        
        for color in cls.car_color:
            
            index = 1

            print_color(f"{color}", "m")
            
            for car, car_information in car_data.items():
                if color == car_information["color"]:
                    print_color(f'{index}. CarID: {car} --- Car Brand: {car_information["brand"]} --- Car model: {car_information["model"]} --- Car year: {car_information["year"]} --- Car km: {car_information["km"]} --- Car quantity: {car_information["quantity"]} --- Car Price: {car_information["sell_price"]}.', "m")
                    print_color("-" * 40, "b")
                    index += 1
# -------------------- #

    @classmethod
    def sort_car_brand(cls):
        data = cls.read_car()


        car_data_brand = []
            
        for car in data.values():
            car_data_brand.append(car["brand"])

        for color in car_data_brand:
            cls.car_brand.add(color)

        return cls

# -------------------- #

    @classmethod
    def sort_car_by_brand(cls):
        cls.sort_car_brand()
        car_data = cls.read_car()
        
        for brand in cls.car_brand:
            
            index = 1

            print_color(f"{brand}", "m")
            
            for car, car_information in car_data.items():
                if brand == car_information["brand"]:
                    print_color(f'{index}. CarID: {car} --- Car color: {car_information["color"]} --- Car model: {car_information["model"]} --- Car year: {car_information["year"]} --- Car km: {car_information["km"]} --- Car quantity: {car_information["quantity"]} --- Car Price: {car_information["sell_price"]}.', "m")
                    print_color("-" * 40, "b")
                    index += 1

# -------------------- #

    @staticmethod
    def read_car(path: str="car"):
        data = ReadWriteData.read(path)

        return data

# -------------------- #

    @staticmethod
    def write_car(data, path: str="car"):
        ReadWriteData.write(data, path)

# -------------------- #

    @staticmethod
    def add_car(brand:str, model, year, color, km, plate, buy_price: float, quantity: int):
        car_data = Car.read_car()

        if car_data:
            max_id = max([int(cid) for cid in car_data.keys()])
            car_id = str(max_id + 1)

        else:
            car_id = "100101"
        
        sell_price = round(buy_price * 1.3, 2)

        car_data[car_id] = {
            "brand" : brand.title(),
            "model" : model,
            "year" : year,
            "color" : color,
            "km" : km,
            "plate" : plate,
            "quantity" : quantity,
            "buy_price" : buy_price,
            "sell_price" : sell_price
        }

        Car.write_car(car_data)
# -------------------- #

    staticmethod
    def show_cars():
        data = Car.read_car()

        index = 1

        for car_id, car_info in data.items():

            if car_info["quantity"] > 0:

                print_color(f"{index}. Car brand: {car_id} --- brand: {car_info['brand']} --- model: {car_info['model']} --- color: {car_info['color']} --- year: {car_info['year']} --- quantity: {car_info['quantity']} --- price: {car_info['sell_price']}", "m")

                index += 1

                print_color("-" * 40, "b")

# -------------------- #

# --------------------------------------------------------- #

class User:

    def __init__(self, username: str):
        self.username = username

        self.all_user = User.read_user()
        self.user_info = self.all_user[username]

        self.password = self.user_info["password"]
        self.name = self.user_info["name"]
        self.email = self.user_info["email"]
        self.permission = self.user_info["permission"]
        self.balance = self.user_info["balance"]

# -------------------- #

    def change_balance(self, amount: int, mode: str="buy", admin: str="mhghasri"):
        
        user_data = User.read_user()

        if mode == "buy":
            user_data[self.username]["balance"] -= amount

            user_data[admin]["balance"] += amount

        elif mode == "charge":
            user_data[self.username]["balance"] += amount


        elif mode == "sell":
            user_data[self.username]["balance"] += amount

            user_data[admin]["balance"] -= amount

        elif mode == "admin_buy":

            user_data[admin]["balance"] -= amount


        else:
            raise ValueError("Invalid input for mode in User.change_balance.")

        User.write_user(user_data)        
        
# -------------------- #

    def show_balance(self):
        print_color(f"Account: {self.username}. Current balance: '{self.balance}'$.", "g")

# -------------------- #

    def charg_balance(self):

        amount = int(input("\nPlease enter amount of money for deposite: "))


        self.change_balance(amount= amount, mode= "charge")

        print_color(f"{self.username} you deposite '{amount}'$ successfully. current balance: {self.balance + amount}.", "g")

# -------------------- #

    @staticmethod
    def read_user(path: str="user"):
        
        data = ReadWriteData.read(path)

        return data

# -------------------- #

    @staticmethod
    def write_user(data, path: str="user"):
        ReadWriteData.write(data, path)

# -------------------- #
    @staticmethod
    def add_user():

        all_user = User.read_user()

        while True:

            username = input("\nPlease enter your user name: ")

            if username not in all_user.keys():
                print_color(f"Wellcome dear {username}.", "g")
                break

            else:
                print_color("This user name already exist. please choose another user name.")

            
        for number in range(3, 0, -1):
            
            password = input("\nPlease enter your password: ")

            if User.password_validation(password):
                print_color(f"Your password accepted. Username: {username} --- Password: {password}.", "g")
                break
                
            elif number == 1:
                print_color("Out of chance. Please try again later.")
                return False
                
            else:
                print_color(f"Please try again. {number - 1} time reamaning.")

        fname = input("\nPlease enter your first name: ")

        lname = input("\nPlease enter your last name: ")

        email = input("\nPlease enter your email: ")

        all_user[username] = {
            "password" : password,
            "name" : f"{fname}_{lname}",
            "email" : email,
            "permission" : "user",
            "balance" : 0
        }

        User.write_user(data= all_user)

# -------------------- #

    @staticmethod
    def password_validation(password: str):
        lower = upper = digit = other = 0

        for ch in password:
            if ch.islower():
                lower += 1

            elif ch.isupper():
                upper += 1

            elif ch.isdigit():
                digit += 1

            else:
                other += 1

        if len(password) in range(8, 33):
            if (lower >= 1) and (upper >= 1) and (digit >= 1) and (other >= 1):
                return True

            else:
                print_color("Your password must be at least one character (lower, upper, digit, other) cases.")
                return False

        else:
            print_color("Your password must be 8-32 character.")
            return False

# -------------------- #

    @staticmethod
    def login():
        user_data = User.read_user()

        while True:

            username = input("\nEnter your user name: ")

            if username in user_data.keys():
                print_color(f"Wellcome back dear {username}.", "g")
                break

            else:
                print_color("Invalid user name. please try again.")


        for numebr in range (3, 0, -1):
            password = input(f"\nEnter your password {username}: ")

            if password == user_data[username]["password"]:
                print_color(f"Login successfully. User name: {username} --- Password: {password}", "g")
                return username

            elif numebr == 1:
                print_color("Out of chance. Please try agian later.")
                return False

            else:
                print_color(f"Invalid password. Please try again, {numebr - 1} time remaining.")

# -------------------- #
    @staticmethod
    def admin_or_user(username):
        data = User.read_user()

        if data[username]["permission"] == "admin":
            return "admin"

        elif data[username]["permission"] == "user":
            return "user"

# -------------------- #

    @staticmethod
    def show_cars():
        Car.show_cars()

# -------------------- #

    @staticmethod
    def show_cars_sorted_by_color():
        Car.sort_car_by_color()

# -------------------- #

    @staticmethod
    def show_cars_sorted_by_brand():
        Car.sort_car_by_brand()

# -------------------- #

# --------------------------------------------------------- #

class Admin(User):
    def __init__(self, username):
        super().__init__(username)

# -------------------- #

    def add_car(self):
        
        brand = input("\nPlease enter car brand: ")

        model = input(f"\nPlease enter model of {brand}: ")

        color = input(f"\nPlease enter color of car: ")

        year = input(f"\nPlease enter year of car: ")

        km = input(f"\nPlease enter car km for selling: ")

        plate = input(f"\nPlease enter car plate: ")

        buy_price = int(input(f"\nPlease enter a buy price: "))

        quantity = int(input(f"\nPlease enter quantity of you want add: "))

        amount = quantity * buy_price

        if self.balance >= amount:

            current_balance = self.balance - amount
            
            print_color(f"You buy seccusefully new car(s). current balance: {current_balance}.", "g")

        else:
            print_color(f"not enough balance. current balance: {self.balance}.")

            new_quantity = self.balance // buy_price

            print_color(f"Dear {self.username} You can buy just {new_quantity} car.", "y")

            while True:
                
                yes_or_no = input(f"\nDo you want buy it? (yes/no): " ).lower()

                if yes_or_no in ("yes", "no"):
                    if yes_or_no == "yes":

                        amount = buy_price * new_quantity

                        current_balance = self.balance - amount

                        print_color(f"You buy seccusefully new car(s). current balance: {current_balance}.", "g")

                        break

                    else:
                        print_color("buying is successfully canceled.", "g")

                        return None


                else:
                    print_color("Invalid input please try again.")

            

            

        Car.add_car(brand, model, year, color, km, plate, buy_price, quantity)
        self.change_balance(amount, mode="admin_buy")

# -------------------- #

    def edit_car(self):

        car_data = Car.read_car()
        
        Car.show_cars()

        print_color(f"Dear {self.username} This are all car galery.", "y")


        while True:
            edit_option = input("\nPlease enter Car ID for editing: ")

            if edit_option in car_data.keys():
                
                car = Car(edit_option)
                car.edit_car()

                break

            else:
                print_color("Wrong input please try again.")

# -------------------- #

    def panel(self):
        print_color(f"Wellcome admin. '{self.username}' --- '{current_time}'.", "y")
        while True:
            print_color("1. car galary\n2. add new car\n3. edit cars\n4. show car dealing list\n5. show balance\n6. show car sorted by color\n7. show car sorted by brand\n8. log out", "y")

            admin_option = input("\nPlease enter your option: ")

            if admin_option in "12345678":
                
                if admin_option == "1":
                    self.show_cars()
                
                elif admin_option == "2":
                    self.add_car()
                
                elif admin_option == "3":
                    self.edit_car()
                
                elif admin_option == "4":
                    self.show_car_dealing_list()
                
                elif admin_option == "5":
                    self.show_balance()
                
                elif admin_option == "6":
                    self.show_cars_sorted_by_color()
                
                elif admin_option == "7":
                    self.show_cars_sorted_by_brand()
                
                elif admin_option == "8":
                    print_color("log out successfully.", "g")
                    return None
            else:
                print_color("Invalid input. Please try again.")
# -------------------- #

    @staticmethod
    def show_cars():

        print_color(f"This is quantity of Mh galery.", "y")
        
        car_data = Car.read_car()

        index = 1

        for car_id, car_info in car_data.items():

            print_color(f"{index}. Car brand: {car_id} --- brand: {car_info['brand']} --- model: {car_info['model']} --- color: {car_info['color']} --- year: {car_info['year']} --- quantity: {car_info['quantity']} --- sell_price: {car_info['sell_price']} --- buy_price: {car_info['buy_price']}", "m")

            index += 1

            print_color("-" * 40, "b")

# -------------------- #

    @staticmethod
    def show_car_dealing_list():
        dealing_data = CarDealingList.read_dealings()

        index = 1

        for deal_id, deal_info in dealing_data.items():

            print_color(f"{index}. Deal Id: {deal_id} --- buyer: {deal_info['buyer']} --- car Id: {deal_info['car_id']} --- deal_date: {deal_info['time']} --- final price: {deal_info['final_price']}$ --- profit: {deal_info['profit']}.", "y")

            index += 1

            print_color("-" * 40, "b")

# -------------------- #

# --------------------------------------------------------- #

class BasicUser(User):
    def __init__(self, username):
        super().__init__(username)


    def buy_car(self):

        car_data = Car.read_car()

        dealing_data = CarDealingList.read_dealings()

        print_color(f"Dear {self.username}Wellcome to buying car.", "c")

        self.show_cars()

        while True:
            car_id = input("\nPlease enter car id for buying: ")

            if car_id in car_data.keys():

                car_choosen = Car(car_id)
                
                print_color("You choose this car: ", "c")

                print_color(f"Id: {car_choosen.car_id} --- brand: {car_choosen.car_brand} --- price: {car_choosen.car_sell_price} --- quantity: {car_choosen.quantity}.", "c")

                break                

            else:
                print_color("This Id is not exist. Please enter valid id.")


        while True:
            
            quantity = int(input("\nPlease enter quantity of you want: "))

            if quantity <= car_choosen.quantity:
                break

            else:
                print_color("not enough quantity.")

        amount = quantity * car_choosen.car_sell_price

        if self.balance >= amount:
            
            amount = quantity * car_choosen.car_sell_price

        else:
            print_color(f"Not enough money. {self.username} you need to charge your balance. current balance: '{self.balance}'$.")

            quantity = self.balance // car_choosen.car_sell_price

            print_color(f"But you can buy '{quantity}' car(s) with id: {car_id}.", "g")

            while True:

                user_want_new_amount = input("\nDo you want it? (yes, no): ")

                if user_want_new_amount in ("yes", "no"):
                    
                    if user_want_new_amount == "yes":
                        
                        amount = quantity * car_choosen.car_sell_price

                        break



                    else:
                        print_color("buying Transaction successfully canceled.", "g")

                        return False

                else:
                    
                    print_color("Invalid input.")

        self.change_balance(amount= amount, mode="buy")

        car_data[car_id]["quantity"] -= quantity


        profit = amount - (quantity * car_choosen.car_buy_price)


        if dealing_data:
            max_id = max([int(cid) for cid in dealing_data.keys()])
            dealing_id = str(max_id + 1)

        else:
            dealing_data = "200202"

        dealing_data[dealing_id] = {
            "buyer" : self.username,
            "car_id" : car_id,
            "quantity" : quantity,
            "final_price" : amount,
            "time" : current_time,
            "car_information" : {
                "brand" : car_choosen.car_brand,
                "model" : car_choosen.car_model,
                "color" : car_choosen.car_color,
                "plate" : car_choosen.car_plate,
                "km" : car_choosen.car_km,
                "year" : car_choosen.car_year
            },
            "profit" : profit
        }

                        
        car_choosen.write_car(car_data)

        CarDealingList.write_dealings(dealing_data)

        print_color(f"you buy successfully new car. current balance: '{self.balance}'$.", "g")

        print_color(f"car id: {car_id} --- brand: {car_choosen.car_brand} --- model: {car_choosen.car_model} --- color: {car_choosen.car_color} --- quantity: {car_choosen.quantity} --- final_price: {amount}.", "c")

# -------------------- #

    def panel(self):
        pass

# -------------------- #

    def show_all_dealing(self):

        dealing_data = CarDealingList.read_dealings()

        flag = False

        index = 1

        for dealing_id, dealing_info in dealing_data.items():

                if self.username == dealing_info["buyer"]:

                    print_color(f'{index}. deal id: {dealing_id} --- car id: {dealing_info["car_id"]} --- final price: {dealing_info["final_price"]}$ --- time of dealing: {dealing_info["time"]}', "c")

                    print_color(f"Brand: {dealing_info['car_information']['brand']} --- model: {dealing_info['car_information']['model']} --- color: {dealing_info['car_information']['color']} --- year: {dealing_info['car_information']['year']} --- km: {dealing_info['car_information']['km']} --- plate: {dealing_info['car_information']['plate']}", "c")

                    index += 1

                    flag = True

                    print_color("-" * 40, "b")

        if not flag:
            print_color(f"{self.username} you dont have any dealing.")

# -------------------- #

    def refund(self):

        pass

# --------------------------------------------------------- #

ali = BasicUser("alinorouzi")

ali.show_all_dealing()

print(ali.username)
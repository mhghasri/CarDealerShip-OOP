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

class MySQLDB:
    

    def __init__(self):
        
        self.connection = pymysql.connect(host= 'localhost', user= 'root', passwd= '', database= 'cardealership') 


    def get_cursor(self):
        return self.connection.cursor()


    def select(self, query, paramas=None):

        cursor = self.get_cursor()

        cursor.execute(query, paramas)    

        result = cursor.fetchall()

        cursor.close()

        return result   


    def creat_record(self, query, paramas):
        cursor = self.get_cursor()

        cursor.execute(query, paramas)

        self.connection.commit()

        cursor.close()


    def update_record(self, query, paramas):
        cursor = self.get_cursor()

        cursor.execute(query, paramas)

        self.connection.commit()

        cursor.close()


    def close(self):
        self.connection.close()

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
        
        elif path_type == "refund":
            return "./json/RefundDealingList.json"
        
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

# -------------------- #

    @staticmethod
    def show_selected_deal(user_id):
        
        dealing_data = CarDealingList.select_choosen_deal(user_id)

        if dealing_data:
            print_color("Your car buying is:", "c")

            for index, car_info in enumerate(dealing_data, start=1):

                car_id = car_info[2]

                car = Car(car_id)

                print_color(f"{index}. Dealing Id: {car_info[0]} --- Car Id: {car_info[2]} --- quantiy: {car_info[3]} --- final price: {car_info[4]} --- Time: {car_info[5]}.", "m")

                print_color(f"brand: {car.car_brand} --- model: {car.car_model} --- color: {car.car_color} --- price: '{car.car_sell_price}'$.", "c")

                print_color("-" * 40, "b")

        else:
            print_color("You dont have any car.")

# -------------------- #

    @staticmethod
    def show_all_deal():
        data = CarDealingList.select_all_deal()

        for index, car_info in enumerate(data, start= 1):

            buyer = User.select_user_by_id(car_info[1])

            car = Car(car_info[2])

            print_color(f"{index}. Dealing Id: {car_info[0]} --- Buyer_Id: {car_info[1]} --- Car Id: {car_info[2]} --- quantiy: {car_info[3]} --- final price: {car_info[4]} --- Time: {car_info[5]} --- profit: {car_info[6]}", "m")

            print_color(f"Buyer: {buyer[1]} --- car brand: {car.car_brand} --- car model: {car.car_model} --- car color: {car.car_color}.", "y")

            print_color("-" * 40, "b")
            

# -------------------- #

    @staticmethod
    def select_all_deal():
        query = "select * from car_dealing_lists"

        db = MySQLDB()

        result = db.select(query)

        db.close()

        return result

# -------------------- #

    @staticmethod
    def select_choosen_deal(user_id):
        query = "select * from car_dealing_lists where Buyer = %s"

        paramas = user_id

        db = MySQLDB()

        result = db.select(query=query, paramas=paramas)
        
        return result
# -------------------- #

    @staticmethod
    def create_new_deal(buyer, carid, quantity, final_price, profit):

        query = "insert into car_dealing_lists (Buyer, CarId, Quantity, FinalPrice, Profit) values (%s, %s, %s, %s, %s)"

        paramas = (buyer, carid, quantity, final_price, profit)

        db = MySQLDB()

        db.creat_record(query, paramas)

        db.close()

# -------------------- #

    @staticmethod
    def read_dealings(path: str="deal"):
        data = ReadWriteData.read(path)

        return data
    
# -------------------- #

    @staticmethod
    def write_dealings(data, path: str= "deal"):
        ReadWriteData.write(data, path)

# --------------------------------------------------------- #

class RefundDealingList:

    @staticmethod
    def read_refund(path: str="refund"):
        data = ReadWriteData.read(path)

        return data
    
    @staticmethod
    def write_refund(data, path: str="refund"):
        ReadWriteData.write(data, path)


# --------------------------------------------------------- #

class Car:

    car_color = set()
    car_brand = set()

    def __init__(self, car_id):
        self.car_id = car_id

        self.car_information = self.select_choosen_car()

        self.car_brand = self.car_information[1]
        self.car_model = self.car_information[2]
        self.car_year = self.car_information[3]
        self.car_color = self.car_information[4]
        self.car_km = self.car_information[5]
        self.car_plate = self.car_information[6]
        self.quantity = self.car_information[7]
        self.car_buy_price = self.car_information[8]
        self.car_sell_price = self.car_information[9]

# -------------------- #

    def select_choosen_car(self):

        query = f"select * from cars where CarId = '{self.car_id}'"

        db = MySQLDB()

        result = db.select(query)

        return result[0]

# -------------------- #

    def update_choosen_car(self, brand, model, year, color, km, plate, quantity, buy_price, sell_price):

        query = "update cars set brand = %s, model = %s, year = %s, color = %s, km = %s, plate = %s, quantity = %s, buyPrice = %s, sellPrice = %s where CarId = %s"

        paramas = (brand, model, year, color, km, plate, quantity, buy_price, sell_price, self.car_id)

        db = MySQLDB()

        db.update_record(query, paramas)
        
# -------------------- #

    def edit_car(self):


        admin = Admin("mhghasri")

        old_amount = self.car_buy_price * self.quantity
        
        brand = input("\nEnter brand of car: ").title()
        model = input("\nEnter model of car: ")
        year = input("\nEnter year of car: ")
        color = input("\nEnter color of car: ")
        km = input("\nEnter km of car: ")
        plate = input("\nEnter plate of car: ")
        quantity = int(input("\nEnter quantity of car: "))
        buy_price = int(input("\nEnter buy price of car: "))
        sell_price = buy_price * 1.3


        current_amount = quantity * buy_price


        new_amount = current_amount - old_amount



        if admin.balance >= new_amount:

            self.update_choosen_car(brand, model, year, color, km, plate, quantity, buy_price, sell_price)

            admin.update_balance(amount= new_amount, mode="admin_buy")

            print_color("Car edited successfully.", "g")

            


        else:

            print_color(f"not enough money. current money is '{admin.balance}$'")

            return False

# -------------------- #

    @classmethod
    def sort_car_color(cls):
        data = cls.select_all_cars()


        car_data_color = []
            
        for car in data:
            car_data_color.append(car[4])

        for color in car_data_color:
            cls.car_color.add(color)

        return cls
    
# -------------------- #

    @staticmethod
    def create_new_car_record(brand, model, year, color, km, plate, quantity, buy_price, sell_price):

        query = "insert into cars (brand, model, year, color, km, plate, quantity, buyprice, sellprice) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        paramas = (brand, model, year, color, km, plate, quantity, buy_price, sell_price)

        db = MySQLDB()

        db.creat_record(query, paramas)

        db.close()

# -------------------- #

    @classmethod
    def sort_car_by_color(cls):
        cls.sort_car_color()
        car_data = cls.select_all_cars()
        
        for color in cls.car_color:
            
            index = 1

            print_color(f"{color}", "m")
            
            for car_information in car_data:
                if color == car_information[4]:

                    print_color(f'{index}. CarID: {car_information[0]} --- Car Brand: {car_information[1]} --- Car model: {car_information[2]} --- Car year: {car_information[3]} --- Car km: {car_information[4]} --- Car quantity: {car_information[7]} --- Car Price: {car_information[9]}.', "m")
                    print_color("-" * 40, "b")
                    index += 1
# -------------------- #

    @classmethod
    def sort_car_brand(cls):
        data = cls.select_all_cars()


        car_data_brand = []
            
        for car in data:
            car_data_brand.append(car[1])

        for brand in car_data_brand:
            cls.car_brand.add(brand)

        return cls

# -------------------- #

    @classmethod
    def sort_car_by_brand(cls):
        cls.sort_car_brand()
        car_data = cls.select_all_cars()
        
        for brand in cls.car_brand:
            
            index = 1

            print_color(f"{brand}", "m")
            
            for car_information in car_data:
                if brand == car_information[1]:

                    print_color(f'{index}. CarID: {car_information[0]} --- Car model: {car_information[2]} --- color: {car_information[4]} --- Car year: {car_information[3]} --- Car km: {car_information[4]} --- Car quantity: {car_information[7]} --- Car Price: {car_information[9]}.', "m")
                    print_color("-" * 40, "b")
                    index += 1


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
        data = Car.select_all_cars()

        index = 1

        for car_info in data:

            if car_info[7] > 0:

                print_color(f"{index}. Car ID: {car_info[0]} --- brand: {car_info[1]} --- model: {car_info[2]} --- color: {car_info[5]} --- year: {car_info[4]} --- plate: {car_info[6]} --- quantity: {car_info[7]} --- sell_price: '{car_info[9]}'$.", "m")

                index += 1

                print_color("-" * 40, "b")

# -------------------- #

    @staticmethod
    def select_all_cars():

        query = "select * from cars"

        db = MySQLDB()

        return db.select(query)

# -------------------- #

# --------------------------------------------------------- #

class User:

    def __init__(self, username: str):
        self.username = username

        user_data = self.select_all_user()

        user_info = user_data[0]

        self.UserId = user_info[0]

        self.password = user_info[2]

        self.name = user_info[3]

        self.email = user_info[4]

        self.permision = user_info[5]

        self.balance = user_info[6]     
        
# -------------------- #

    def show_dealing_list(self):
        CarDealingList.show_selected_deal(self.UserId)

# -------------------- #

    def select_all_user(self):

        query = f"select * from users where UserName = '{self.username}'"

        db = MySQLDB()

        result = db.select(query)

        db.close()

        return result

# -------------------- #

    def current_balance(self):
        user_data = self.select_all_user()

        user_information = user_data[0]

        current_balance = user_information[6]

        print_color(f"Your current balance is: '{current_balance}'$.", "g")

# -------------------- #

    def update_balance(self, amount: int, mode: str="buy", admin: str="mhghasri"):

        user_data = self.select_choosen_user(self.username)

        admin_data = self.select_choosen_user("mhghasri")

        user_balance  = user_data[6]

        admin_balance = admin_data[6]
    
    
        if mode == "buy":
            user_balance -= amount

            admin_balance += amount

        elif mode == "charge":
            user_balance += amount


        elif mode == "sell":
            user_balance += amount

            admin_balance -= amount

        elif mode == "admin_buy":

            admin_balance -= amount


        else:
            raise ValueError("Invalid input for mode in User.change_balance.")
        
        db = MySQLDB()

        user_query = "update users set Balance = %s where UserName = %s"

        user_params = (user_balance, self.username)

        db.update_record(user_query, user_params)


        if mode in ("buy", "sell", "admin_buy"):
            admin_query = "update users set balance = %s where username = %s"

            admin_params = (admin_balance, admin)

            db.update_record(admin_query, admin_params)

        db.close()

# -------------------- #

    @staticmethod
    def select_user_by_id(user_id):

        query = "select * from users where userid = %s"

        paramas = (user_id)

        db = MySQLDB()

        result = db.select(query, paramas)

        return result[0] 

# -------------------- #

    @staticmethod
    def select_choosen_user(username):

        query = f"select * from users where UserName = '{username}'"

        db = MySQLDB()

        data = db.select(query)

        return data[0]

# -------------------- #

    @staticmethod
    def find_username(username):
        query = f"select * from users where username = '{username}'"

        db = MySQLDB()

        return db.select(query)

# -------------------- #
    
    @staticmethod
    def create_user(username, password, fname, lname, email):
        query = "insert into users (UserName, Password, Name, Email) values (%s, %s, %s, %s)"

        paramas = (username, password, f"{fname} {lname}", email)

        db = MySQLDB()

        db.creat_record(query, paramas)

# -------------------- #
    @staticmethod
    def add_user():


        while True:

            username = input("\nPlease enter your user name: ")
            
            selected_username = User.find_username(username)

            if not selected_username:

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

        User.create_user(username, password, fname, lname, email)

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

        while True:

            username = input("\nEnter your user name: ")

            find_username = User.find_username(username)
            
            if find_username:
                print_color(f"Wellcome back dear {username}.", "g")
                break

            else:
                print_color("Invalid user name. please try again.")


        user_data = User.select_choosen_user(username)

        for numebr in range (3, 0, -1):
            password = input(f"\nEnter your password {username}: ")

            if password == user_data[2]:
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
        data = User.select_choosen_user(username)

        if data[5]== "admin":
            return "admin"

        elif data[5] == "user":
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

    @staticmethod
    def show_refund_cars(username):
        refund_data = RefundDealingList.read_refund()

        flag = False

        index = 1

        for refund_id, refund_info in refund_data.items():

            if username == refund_info["seller"]:

                print_color(f"{index}. Refund Id: {refund_id} --- seller: {refund_info['seller']} --- deal id: {refund_info['dealing_id']} --- final refunded price: {refund_info['final_refund_price']}$ --- quantity: {refund_info['sell_quantity']} --- time refunded: {refund_info['time']}.", "m")

                index += 1

                print_color("-" * 40, "b")

                flag = True

        if not flag:
            print_color("You dont have any refund dealing.")

# -------------------- #

# --------------------------------------------------------- #

class Admin(User):
    def __init__(self, username):
        super().__init__(username)

# -------------------- #

    def show_dealing_list(self):
        CarDealingList.show_all_deal()

# -------------------- #

    def add_car(self):
        
        brand = input("\nPlease enter car brand: ").title()

        model = input(f"\nPlease enter model of {brand}: ")

        color = input(f"\nPlease enter color of car: ")

        year = input(f"\nPlease enter year of car: ")

        km = input(f"\nPlease enter car km for selling: ")

        plate = input(f"\nPlease enter car plate: ")

        buy_price = int(input(f"\nPlease enter a buy price: "))

        quantity = int(input(f"\nPlease enter quantity of you want add: "))

        sell_price = buy_price * 1.3

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

            

            

        Car.create_new_car_record(brand, model, year, color, km, plate, quantity, buy_price, sell_price)
        self.update_balance(amount= amount, mode="admin_buy")

# -------------------- #

    def edit_car(self):
        
        self.show_cars()

        while True:
                
            try:
                edit_option = input("\nPlease enter Car ID for editing: ")

                car = Car(int(edit_option))

            except Exception:
                print_color("Wrong input please try again.")

            else:

                car.edit_car()
                break

# -------------------- #

    def panel(self):
        print_color(f"Wellcome admin. '{self.username}' --- '{current_time}'.", "y")
        while True:
            print_color("1. car galary.\n2. add new car.\n3. edit cars.\n4. show car dealing list.\n5. show balance.\n6. show car sorted by color.\n7. show car sorted by brand.\n8. show refunded list.\n9. log out.", "y")

            admin_option = input("\nPlease enter your option: ")

            if admin_option in "123456789":
                
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
                    self.show_refund_cars()
                
                elif admin_option == "9":
                    print_color("log out successfully.", "g")
                    return None
            else:
                print_color("Invalid input. Please try again.")
# -------------------- #

    @staticmethod
    def show_cars():

        print_color(f"This is quantity of Mh galery.", "y")
        
        car_data = Car.select_all_cars()

        index = 1

        for car_info in car_data:

            print_color(f"{index}. Car ID: {car_info[0]} --- brand: {car_info[1]} --- model: {car_info[2]} --- color: {car_info[4]} --- year: {car_info[3]} --- plate: {car_info[6]} --- quantity: {car_info[7]} --- sell_price: '{car_info[9]}'$ --- buy_price: {car_info[8]}$.", "m")

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

    @staticmethod
    def show_refund_cars():
        refund_data = RefundDealingList.read_refund()

        index = 1

        for refund_id, refund_info in refund_data.items():

            print_color(f"{index}. Refund Id: {refund_id} --- seller: {refund_info['seller']} --- deal id: {refund_info['dealing_id']} --- final refunded price: {refund_info['final_refund_price']}$ --- quantity: {refund_info['sell_quantity']} --- time refunded: {refund_info['time']} --- profit: {refund_info['profit']}.", "y")

            index += 1

            print_color("-" * 40, "b")

# -------------------- #

# --------------------------------------------------------- #

class BasicUser(User):
    def __init__(self, username):
        super().__init__(username)


    def buy_car(self):

        print_color(f"Dear {self.username}. Wellcome to buying car.", "c")

        self.show_cars()

        while True:
            car_id = input("\nPlease enter car id for buying: ")

                
                
            try:

                car_choosen = Car(int(car_id))
                
                print_color("You choose this car: ", "c")

                print_color(f"Id: {car_choosen.car_id} --- brand: {car_choosen.car_brand} --- price: {car_choosen.car_sell_price} --- quantity: {car_choosen.quantity}.", "c")

                break                

            except Exception:
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

        self.update_balance(amount= amount, mode="buy")

        car_choosen.quantity -= quantity


        profit = amount - (quantity * car_choosen.car_buy_price)

        car_choosen.update_choosen_car(car_choosen.car_brand, car_choosen.car_model, car_choosen.car_year, car_choosen.car_color, car_choosen.car_km, car_choosen.car_plate, car_choosen.quantity, car_choosen.car_buy_price, car_choosen.car_sell_price)

        CarDealingList.create_new_deal(self.UserId, car_choosen.car_id, quantity, amount, profit)

        print_color(f"you buy successfully new car. current balance: '{self.balance - amount}'$.", "g")

        print_color(f"car id: {car_id} --- brand: {car_choosen.car_brand} --- model: {car_choosen.car_model} --- color: {car_choosen.car_color} --- quantity: {car_choosen.quantity} --- final_price: {amount}.", "c")

# -------------------- #

    def show_user_dealing(self):

        dealing_data = CarDealingList.read_dealings()

        flag = False

        index = 1

        user_deal_id = []

        for dealing_id, dealing_info in dealing_data.items():

                if self.username == dealing_info["buyer"] and dealing_info["quantity"] > 0:

                    user_deal_id.append(dealing_id)

                    print_color(f'{index}. deal id: {dealing_id} --- car id: {dealing_info["car_id"]} --- quantity: {dealing_info["quantity"]} --- final price: {dealing_info["final_price"]}$ --- time of dealing: {dealing_info["time"]}', "c")

                    print_color(f"Brand: {dealing_info['car_information']['brand']} --- model: {dealing_info['car_information']['model']} --- color: {dealing_info['car_information']['color']} --- year: {dealing_info['car_information']['year']} --- km: {dealing_info['car_information']['km']} --- plate: {dealing_info['car_information']['plate']}", "c")

                    index += 1

                    flag = True

                    print_color("-" * 40, "b")

        if not flag:
            print_color(f"{self.username} you dont have any dealing.")
            return False

        return user_deal_id

# -------------------- #

    def refund(self):

        user_cars = self.show_user_dealing()

        refund_data = RefundDealingList.read_refund()

        dealing_data = CarDealingList.read_dealings()

        car_data = Car.read_car()


        if user_cars:
            
            print_color("Here you are this list is your dealing.", "c")


            while True:

                user_refund_id = input("\nPlease enter your car id for refund: ")
                
                if user_refund_id in user_cars:

                    print_color(f"You choose {user_refund_id}.", "g")


                    while True:

                        are_you_sure = input("\nAre you sure to refund it? you lost 10% for refund the car. (yes/no): ")
                        
                        if are_you_sure in ("yes", "no"):
                            
                            if are_you_sure == "yes":
                                break

                            else:
                                print_color("refund canceled successfully.", "g")
                                return False

                        else:
                            print_color("Invalid input. just ('yes', 'no').")

                    break

                else:
                    print_color("Invalid input. Please enter valid input.")

            
            user_dealing_data = dealing_data[user_refund_id]

            
            while True:

                try: 
                    quantity = int(input("\nPlease enter quantity of you want: "))

                except ValueError:
                    print_color("You must enter integer number !")

                if quantity < user_dealing_data["quantity"]:

                    print_color(f"You are funding '{quantity}' of {user_dealing_data['quantity']}.", "g")

                    break

                elif quantity == user_dealing_data["quantity"]:

                    print_color(f"You sold out all car you have with id: {user_refund_id}.", "g")

                    delet_data_flag = True

                    break



                else:
                    print_color("You cant refund more than you have. Please focus a bit more.")


            one_car_price = user_dealing_data["final_price"] / user_dealing_data["quantity"]

            final_refund_price = (one_car_price * quantity) * 0.9

            refunded_car_id = user_dealing_data["car_id"]

            car_data[refunded_car_id]["quantity"] += quantity 

                
            dealing_data[user_refund_id]["quantity"] -= quantity

            dealing_data[user_refund_id]["final_price"] = one_car_price * (user_dealing_data["quantity"])


            self.change_balance(amount= final_refund_price, mode="sell")

            CarDealingList.write_dealings(dealing_data)
            Car.write_car(car_data)

            if refund_data :
                max_id = max([int(cid) for cid in refund_data.keys()])
                refund_id = str(max_id + 1)

            else:
                refund_id = "300301"

            refund_data[refund_id] = {
                "seller" : self.username,
                "dealing_id" : user_refund_id,
                "time" : current_time,
                "sell_quantity" : quantity,
                "final_refund_price" : final_refund_price,
                "profit" : one_car_price * quantity * 0.1
            }

            RefundDealingList.write_refund(refund_data)
            
# -------------------- #

    def panel(self):
        print_color(f"Wellcome user. '{self.username}' --- '{current_time}'.", "c")
        while True:
            print_color("1. show galary.\n2. buy new car.\n3. show dealing list.\n4. refund car(s).\n5. show refunded car.\n6. show cars sorted by color.\n7. show cars sorted by brand.\n8. current balance.\n9. charge balance.\n10. log out.", "c")

            user_option = input("\nPlease enter your option: ")

            if user_option in "12345678910":
                
                if user_option == "1":
                    self.show_cars()
                
                elif user_option == "2":
                    self.buy_car()
                
                elif user_option == "3":
                    self.show_user_dealing()
                
                elif user_option == "4":
                    self.refund()
                
                elif user_option == "5":
                    self.show_refund_cars(self.username)
                
                elif user_option == "6":
                    self.show_cars_sorted_by_color()
                
                elif user_option == "7":
                    self.show_cars_sorted_by_brand()

                elif user_option == "8":
                    self.show_balance()

                elif user_option == "9":
                    self.charg_balance()
                
                elif user_option == "10":
                    print_color("log out successfully.", "g")
                    return None
            else:
                print_color("Invalid input. Please try again.")

# -------------------- #

# --------------------------------------------------------- #


# bmw = Car(100104)

# bmw.sort_car_by_brand()

mh = Admin("mhghasri")

# mh.show_cars()

ali = BasicUser("alinorouzi")

# ali.buy_car()

# CarDealingList.show_all_deal()

# CarDealingList.show_selected_deal(2)
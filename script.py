from pakages import *
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

class Car:
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
    def add_car(brand, model, year, color, km, plate, buy_price: float, quantity: int):
        car_data = Car.read_data()

        if car_data:
            max_id = max([int(cid) for cid in car_data.keys()])
            car_id = str(max_id + 1)

        else:
            car_id = "100101"
        
        sell_price = round(buy_price * 1.3, 2)

        car_data[car_id] = {
            "brand" : brand,
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


# --------------------------------------------------------- #

class Admin(User):
    pass

# --------------------------------------------------------- #

class BasicUser(User):
    pass

# --------------------------------------------------------- #

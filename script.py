from pakages import *

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


class Car:
    pass

class User:
    def __init__(self, username):
        self.username = username

class Admin(User):
    pass

class BasicUser(User):
    pass


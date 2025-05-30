from colorama import Fore
from datetime import datetime
from time import time
import json
import os
import pymysql

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
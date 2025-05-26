from script import *

print_color("Hello wellcome to our car dealing", "m")

while True:
    print_color("1. signup\n2. log in\n3. exit", "m")

    user_option = input("\nPlease enter your option: ")

    if user_option in "123":
        if user_option == "1":
            User.add_user()

        elif user_option == "2":
            username = User.login()

            if User.admin_or_user(username) == "admin":
                admin = Admin(username)
                admin.panel()

            elif User.admin_or_user(username) == "user":
                user = BasicUser(username)
                user.panel()

        elif user_option == "3":
            print_color("Exiting app. come back later.", "g")
            break

    else:
        print_color("Invalid input. Please enter another input.")
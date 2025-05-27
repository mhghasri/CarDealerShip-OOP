from script import *

print_color("Hello wellcome to our car dealing", "m")

end_time = 0

while True:
    print_color("1. signup\n2. log in\n3. exit", "m")

    try:

        user_option = input("\nPlease enter your option: ")

        flag = True

        if user_option in "123":
            if user_option == "1":
                User.add_user()

            elif user_option == "2":

                current_time = time()

                if (current_time - end_time) > 60:
                    username = User.login()

                    if not username:
                        end_time = time()
                        flag = False

                    if flag:


                        if User.admin_or_user(username) == "admin":
                            admin = Admin(username)
                            admin.panel()

                        elif User.admin_or_user(username) == "user":
                            user = BasicUser(username)
                            user.panel()

                else:

                    time_remainig = int(60 - (current_time - end_time))

                    print_color(f"You are banned for {time_remainig} second(s). Please be pationt!")



            elif user_option == "3":
                print_color("Exiting app. come back later.", "g")
                break

    except ValueError:
        print_color("invalid input.")

    except KeyboardInterrupt:
        print_color("exiting app by user interrupt.", "g")
        break

    else:
        print_color("Invalid input. Please enter another input.")
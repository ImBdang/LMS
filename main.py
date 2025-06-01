from request_handle.login import Login
from request_handle.user import User

def main():
    login = Login()
    tokens = login.login()
    if tokens:
        print("Preparing profile...")

        user = User(tokens)
        user.get_profile()
        user.get_class()
    else:
        return


main()
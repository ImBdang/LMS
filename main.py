from request_handle.login import Login
from request_handle.user import User
from request_handle.lms import LMS

def main():
    print("Welcome to the LMS CLI!\n")
    login = Login()
    tokens = login.login()
    if tokens:
        print("Preparing profile...")

        user = User(tokens)
        user.get_profile()
        user.get_class()
        print("Heading to LMS...")
        
        lms = LMS(user)
        lms.main()
    else:
        return


main()
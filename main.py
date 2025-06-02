from request_handle.login import Login
from request_handle.user import User
from request_handle.lms import LMS
from dotenv import load_dotenv
import json
import os

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(project_root, 'request_handle', '.env')
    load_dotenv(dotenv_path=dotenv_path)

    TOKEN_FILE = os.getenv("TOKEN_FILE")
    token_path = os.path.join(project_root, TOKEN_FILE)

    isConnected = False
    tokens = None
    print("Welcome to the LMS CLI!\n")
    login = Login()
    if not os.path.exists(token_path):
        print("No token file found. Please log in.")
        tokens = login.login(token_path)
    elif os.path.getsize(token_path) == 0:
        print("Token file is empty. Please log in again.")
        tokens = login.login(token_path)
    else:
        with open(token_path, "r") as token_file:
            tokens = json.load(token_file)

    isConnected = login.checkTokens(tokens)

    if not isConnected:
        tokens = login.login(token_path)

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
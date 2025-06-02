from request_handle.login import Login
from request_handle.user import User
from request_handle.lms import LMS
from dotenv import load_dotenv
import json
import os

def main():
    load_dotenv(dotenv_path="request_handle/.env")
    TOKEN_FILE = os.getenv("TOKEN_FILE")
    isConnected = False
    tokens = None
    print("Welcome to the LMS CLI!\n")
    login = Login()
    if not os.path.exists(TOKEN_FILE):
        print("No token file found. Please log in.")
        tokens = login.login()
    elif os.path.getsize(TOKEN_FILE) == 0:
        print("Token file is empty. Please log in again.")
        tokens = login.login()
    else:
        with open(TOKEN_FILE, "r") as token_file:
            tokens = json.load(token_file)

    isConnected = login.checkTokens(tokens)

    if not isConnected:
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
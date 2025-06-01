from dotenv import load_dotenv
from .crc32 import return_signature
import os
import getpass
import requests


class Login: 
    def __init__(self):
        load_dotenv()
        self.url_login = os.getenv("login-url")
        self.x_app_id = os.getenv("x-app-id")
        self.domain = os.getenv("domain")
        self.host = os.getenv("host")
        self.head = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "", 
            "content-type": "application/json",
            "host": self.host,
            "origin": self.domain,
            "referer": self.domain + "/",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-app-id": self.x_app_id,
            "x-request-signature": ""
        }
    
    def login(self):
        self.username = input("Tai khoan: ")
        self.password = getpass.getpass("Mat khau: ")
        self.body = {
            "username": self.username,
            "password": self.password
        }
   
        self.head["x-request-signature"] = return_signature(
            method="POST",
            url=self.url_login,
            body=self.body
        )
        response = requests.post(
            url=self.url_login,
            json=self.body,
            headers=self.head
        )
  
        if response.status_code == 200:
            print("Request succesfully!")
            response_data = response.json()
            print(response_data.get("message"))
            access_token = response_data.get("access_token")
            refresh_token = response_data.get("refresh_token")
            if access_token and refresh_token:
                print("Token has been received")
                token = {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
                return token
            else:
                print("Not found tokens in response")
                return None
        else:
            print("Request failed!")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    


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
        self.sec_ch_ua = os.getenv("sec-ch-ua")
        self.sec_ch_ua_mobile = os.getenv("sec-ch-ua-mobile")
        self.sec_ch_ua_platform = os.getenv("sec-ch-ua-platform")
        self.sec_fetch_dest = os.getenv("sec-fetch-dest")
        self.sec_fetch_mode = os.getenv("sec-fetch-mode")
        self.sec_fetch_site = os.getenv("sec-fetch-site")
        self.user_agent = os.getenv("user-agent")
        self.head = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "", 
            "Content-Type": "application/json",
            "Host": self.host,
            "Origin": self.domain,
            "Referer": self.domain + "/",
            "Sec-Ch-Ua": self.sec_ch_ua,
            "Sec-Ch-Ua-Mobile": self.sec_ch_ua_mobile,
            "Sec-Ch-Ua-Platform": self.sec_ch_ua_platform,
            "Sec-Fetch-Dest": self.sec_fetch_dest,
            "Sec-Fetch-Mode": self.sec_fetch_mode,
            "Sec-Fetch-Site": self.sec_fetch_site,
            "User-Agent": self.user_agent,
            "X-App-Id": self.x_app_id,
            "X-Request-Signature": ""
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
            print("Request failed")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    


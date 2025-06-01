from dotenv import load_dotenv
from .crc32 import return_signature
import os
import requests

class User:
    def __init__(self, tokens):
        load_dotenv()
        self.access_token = tokens.get("access_token")
        self.refresh_token = tokens.get("refresh_token")
        self.profile_url = os.getenv("profile-url")
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
        self.class_url = os.getenv("class-url")
        self.classes_url = os.getenv("classes-url")
        self.head = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Bearer " + self.access_token, 
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
            "X-Request-Signature": return_signature(
                method="GET",
                body={}
            )
        }

    def get_profile(self):
        response = requests.get(
            url=self.profile_url,
            headers=self.head
        )
        if response.status_code == 200:
            response_data = response.json()
            self.user = {
                "id": response_data.get("data")[0].get("id"),
                "name": response_data.get("data")[0].get("full_name"),
            }
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return 
    
    def get_class(self):
        query_params = {
            "limit": 1000,
            "paged": 1,
            "select": "namhoc,hocky,class_id",
            "condition[0][key]": "student_id",
            "condition[0][value]": self.user.get("id"), 
            "condition[0][compare]": "=" 
        }
        self.head["X-Request-Signature"] = return_signature(
            method="GET",
            body={}
        )
        response = requests.get(
            url=self.class_url,
            headers=self.head,
            params=query_params
        )
        if response.status_code == 200:
            response_data = response.json()
            self.classes = {
                "hocky": response_data.get("next"),
                "classes": response_data.get("data")
            }
            classes_list = []
            for i in self.classes.get("classes"):
                if self.classes.get("hocky") == i.get("hocky"):
                    classes_list.append(str(i.get("class_id")))
            classes_text = ",".join(classes_list)

            self.head["X-Request-Signature"] = return_signature(
                method="GET",
                body={}
            )
            res = requests.get(
                url=self.classes_url,
                headers=self.head,
                params = {
                    "select": "id,sotinchi,course_id,name,time_start,time_end,hocky,namhoc",
                    "limit": 1000,
                    "paged": 1,
                    "include": classes_text,
                    "include_by": "id"
                }
            )
            if res.status_code == 200:
                res_data = res.json()
                self.courses = res_data.get("data")
        
            else:
                print(f"Error: {res.status_code} - {res.text}")
                return
           
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return

    def get_courses(self):
        coures = self.courses
        return coures

    
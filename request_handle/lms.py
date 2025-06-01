from dotenv import load_dotenv
from .crc32 import return_signature
import os

class LMS:
    def __init__(self, user):
        load_dotenv()
        self.user = user
        self.courses = user.get_courses()
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
            "Authorization": "Bearer " + self.user.access_token, 
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

    def view_courses(self):
        if not self.courses:
            print("No courses available.")
            return
        print("\nAvailable Courses:")
        for idx, course in enumerate(self.courses, start=1):
            print(f"{idx}. {course['name']} (ID: {course['id']})")
    
    def main(self):
        isAble = False
        yourCourse = None
        while True:
            self.view_courses()
            choice = int(input("Chon ID mon hoc: "))
            for i in self.courses:
                if choice == i.get("id"):
                    print(f"ID mon hoc ban chon la: {choice}\nMon: {i.get('name')}")
                    yourCourse = i
                    isAble = True
                    input("Nhan Enter de tiep tuc...")
                    break
            else:
                print("ID mon hoc khong hop le.")
                input("Nhan Enter de tiep tuc...")
            
            if isAble:
                print("Bat dau hoc...")
                for lesson in yourCourse:
                    print(lesson)
                input("Nhan Enter de tiep tuc...")
     
from dotenv import load_dotenv
from .crc32 import return_signature
import requests
import os

class LMS:
    def __init__(self, user):
        load_dotenv()
        self.sysname = os.name
        self.clear_command = "cls" if self.sysname == "nt" else "clear"
        self.class_plan_url = os.getenv("class-plan-url")
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
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "Bearer " + self.user.access_token, 
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
            os.system(self.clear_command)
            print("\nNhap 0 de thoat khoi chuong trinh.")
            self.view_courses()
            choice = int(input("Chon ID mon hoc: "))
            for i in self.courses:
                if choice == i.get("id"):
                    os.system(self.clear_command)
                    print(f"ID mon hoc ban chon la: {choice}\nMon: {i.get('name')}")
                    yourCourse = i
                    isAble = True
                    input("Nhan Enter de tiep tuc...")
                    break
            if choice == 0:
                print("Exiting...")
                break
                
            elif not isAble:
                os.system(self.clear_command)
                print("ID mon hoc khong hop le.")
                input("\nNhan Enter de tiep tuc...")
            
            if isAble:
                self.get_class_plan(yourCourse)

    def get_class_plan(self, course):
        self.head["X-Request-Signature"] = return_signature(
            method="GET",
            body={}
        )
        response = requests.get(
            url=self.class_plan_url,
            headers=self.head,
            params = {
                "limit": 1000,
                "paged": 1,
                "orderby": "week",
                "order": "ASC",
                "select": "id,class_id,course_id,course_plan_activity_id,week,title,date_start_of_week,date_end_of_week,teaching_day",
                "condition[0][key]": "class_id",
                "condition[0][value]": course.get("id"),
                "condition[0][compare]": "=",
                "condition[1][key]": "week",
                "condition[1][value]": "1000",
                "condition[1][compare]": "<>"
            }
        )
        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get("data")
            while True:
                os.system(self.clear_command)
                print("Nhap 0 de exit")
                print(f"So luong tuan hoc la {response_data.get('count')}, vui long chon tuan hoc ban muon: ")
                week = int(input("Nhap tuan hoc: "))
                if week == 0:
                    print("Exiting...")
                    break
                elif 1 <= week <= response_data.get("count"):
                    print(data[week-1])
                    input("\nNhan Enter de tiep tuc...")
                else:
                    print("Tuan hoc khong hop le, vui long nhap lai.")
                    input("\nNhan Enter de tiep tuc...")

        else:
            print(f"Error fetching class plan: {response.status_code} - {response.text}")
     
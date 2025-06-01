from request_handle.login import Login

def main():
    login = Login()
    tokens = login.login()
    if tokens:
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
    else:
        return
    

main()
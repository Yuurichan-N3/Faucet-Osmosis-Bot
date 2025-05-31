import requests
import time
from colorama import Fore, Style

def poll_captcha(api_key, captcha_id, endpoint):
    try:
        for _ in range(30):
            time.sleep(6)
            response = requests.get(endpoint, params={
                "key": api_key,
                "action": "get",
                "id": captcha_id,
                "json": 1
            })
            response.raise_for_status()
            result = response.json()
            if result["status"] == 1:
                print(f"{Fore.GREEN}Turnstile token obtained!")
                return result["request"]
            if result["request"] != "CAPCHA_NOT_READY":
                raise Exception("2Captcha polling error")
        raise Exception("2Captcha timeout")
    except Exception as e:
        print(f"{Fore.RED}Failed to get Turnstile token: {e}")
        return None
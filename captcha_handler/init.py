import requests
from colorama import Fore

def init_captcha(api_key, site_key, url, endpoint):
    try:
        print(f"{Fore.YELLOW}Sending request to 2Captcha for Turnstile token...")
        response = requests.get(endpoint, params={
            "key": api_key,
            "method": "turnstile",
            "sitekey": site_key,
            "pageurl": url,
            "json": 1
        })
        response.raise_for_status()
        result = response.json()
        if result["status"] != 1:
            raise Exception("2Captcha error")
        return result["request"]
    except Exception as e:
        print(f"{Fore.RED}Failed to init 2Captcha: {e}")
        return None
import json
import time
from colorama import init, Fore, Style
from wallet_ops.gen import generate_new_wallet
from wallet_ops.save import save_wallet
from address_util.conv import convert_to_osmo_address
from captcha_handler.init import init_captcha
from captcha_handler.poll import poll_captcha
from claim_core.claim import claim_faucet
from claim_core.ui import show_banner, get_option

init(autoreset=True)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    show_banner()
    config = load_json("wallet_ops/config.json")
    rules = load_json("address_util/rules.json")
    api = load_json("captcha_handler/api.json")
    endpoints = load_json("captcha_handler/endpoints.json")
    headers = load_json("claim_core/headers.json")
    faucet_url = "https://faucet.testnet.osmosis.zone/api/fund"
    option = get_option()
    if option == "1":
        try:
            num_requests = int(input(f"{Fore.YELLOW}Enter number of wallets to generate and claim: {Style.RESET_ALL}"))
            if num_requests <= 0:
                raise ValueError("Number must be greater than 0")
        except:
            print(f"{Fore.RED}Invalid input")
            return
        for i in range(num_requests):
            print(f"{Fore.YELLOW}Generating wallet {i+1}...")
            cosmos_address, private_key = generate_new_wallet()
            try:
                osmo_address = convert_to_osmo_address(cosmos_address)
            except:
                print(f"{Fore.RED}Failed to convert address")
                continue
            success_count = 0
            for _ in range(5):
                captcha_id = init_captcha(api["api_key"], api["site_key"], faucet_url, endpoints["init"])
                if not captcha_id:
                    print(f"{Fore.RED}Failed to get Turnstile token for {osmo_address}")
                    time.sleep(5)
                    continue
                cf_turnstile_response = poll_captcha(api["api_key"], captcha_id, endpoints["poll"])
                if not cf_turnstile_response:
                    print(f"{Fore.RED}Failed to get Turnstile token for {osmo_address}")
                    time.sleep(5)
                    continue
                result = claim_faucet(osmo_address, cf_turnstile_response, headers, faucet_url)
                if result:
                    success_count += 1
                    if success_count == 1:
                        save_wallet(osmo_address, private_key, config["wallet_file"])
                time.sleep(5)
            if success_count == 0:
                print(f"{Fore.RED}Wallet not saved due to claim failure for {osmo_address}")
    else:
        osmo_address = input(f"{Fore.YELLOW}Enter osmo address: {Style.RESET_ALL}")
        if not osmo_address.startswith(rules["prefix"]):
            print(f"{Fore.RED}Address must start with '{rules['prefix']}'")
            return
        success_count = 0
        while success_count < 10:
            try:
                print(f"{Fore.YELLOW}Claiming for {osmo_address} (Success {success_count}/10)...")
                captcha_id = init_captcha(api["api_key"], api["site_key"], faucet_url, endpoints["init"])
                if not captcha_id:
                    print(f"{Fore.RED}Failed to get Turnstile token for {osmo_address}")
                    time.sleep(5)
                    continue
                cf_turnstile_response = poll_captcha(api["api_key"], captcha_id, endpoints["poll"])
                if not cf_turnstile_response:
                    print(f"{Fore.RED}Failed to get Turnstile token for {osmo_address}")
                    time.sleep(5)
                    continue
                result = claim_faucet(osmo_address, cf_turnstile_response, headers, faucet_url)
                if result:
                    success_count += 1
                time.sleep(5)
            except KeyboardInterrupt:
                print(f"{Fore.YELLOW}Process stopped by user")
                break
        if success_count >= 10:
            print(f"{Fore.GREEN}Completed 10 successful claims for {osmo_address}")

if __name__ == "__main__":
    main()

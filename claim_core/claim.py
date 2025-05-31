import requests
import json
import uuid
from colorama import Fore, Style

def claim_faucet(address, cf_turnstile_response, headers, faucet_url):
    try:
        print(f"{Fore.YELLOW}Sending claim for {address}...")
        response = requests.post(faucet_url, headers=headers, data={
            "address": address,
            "cf-turnstile-response": cf_turnstile_response
        })
        response.raise_for_status()
        tx_hash = str(uuid.uuid4()).replace("-", "").upper()
        result = {
            "status": "Transaction broadcasted",
            "tx_hash": tx_hash,
            "explorer": f"https://www.mintscan.io/osmosis-testnet/tx/{tx_hash}",
            "address": address
        }
        print(f"{Fore.GREEN}Claim for {address}: {json.dumps(result, indent=2)}")
        print(f"{Fore.GREEN}Claim successful for {address}")
        return result
    except:
        print(f"{Fore.RED}Claim failed for {address}")
        return None
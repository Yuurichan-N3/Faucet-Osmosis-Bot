import json

def save_wallet(address, private_key, filename):
    try:
        try:
            with open(filename, "r") as f:
                wallets = json.load(f)
        except FileNotFoundError:
            wallets = []
        wallets.append({"address": address, "private_key": private_key.hex()})
        with open(filename, "w") as f:
            json.dump(wallets, f, indent=4)
        return True
    except:
        return False
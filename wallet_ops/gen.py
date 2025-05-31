from cosmospy import generate_wallet

def generate_new_wallet():
    wallet = generate_wallet()
    return wallet["address"], wallet["private_key"]
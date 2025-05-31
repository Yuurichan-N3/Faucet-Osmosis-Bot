from bech32 import bech32_decode, bech32_encode

def convert_to_osmo_address(cosmos_address):
    hrp, data = bech32_decode(cosmos_address)
    if hrp != "cosmos" or not data:
        raise ValueError("Invalid address")
    return bech32_encode("osmo", data)
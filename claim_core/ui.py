from colorama import Fore, Style

def show_banner():
    banner = f"""
{Fore.CYAN + Style.BRIGHT}╔══════════════════════════════════════════════╗
║         🌟 Osmosis Auto Faucet Bot           ║
║   Automate your Osmosis testnet claims!      ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def get_option():
    while True:
        print(f"{Fore.YELLOW}Select option:")
        print(f"{Fore.YELLOW}1. Generate new wallet and claim")
        print(f"{Fore.YELLOW}2. Claim repeatedly for single address")
        option = input(f"{Fore.YELLOW}Enter choice (1 or 2): {Style.RESET_ALL}")
        if option in ["1", "2"]:
            return option
        print(f"{Fore.RED}Invalid choice. Enter 1 or 2.")

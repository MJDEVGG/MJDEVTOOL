# ===[ KEY SYSTEM ADDITION — DO NOT REMOVE OR EDIT EXISTING CODE ]===
import requests, json, time, os

API_URL = "https://mjpanel.42web.io/keys.json"  # 🔗 change this to your PHP API URL

def check_key_valid(key):
    """Check key validity + mark as used via PHP API"""
    try:
        res = requests.post(API_URL, json={"action": "list", "admin_pass": "admin123"})
        data = res.json()
        if not data.get("success"):
            print("❌ Server error:", data.get("message"))
            return False

        for k in data.get("keys", []):
            if k["key"] == key:
                if k.get("used", False):
                    print("❌ This key has already been used!")
                    return False
                # mark key as used
                mark = requests.post(API_URL, json={
                    "action": "mark_used",
                    "admin_pass": "admin123",
                    "key": key
                })
                mark_data = mark.json()
                if mark_data.get("success"):
                    print("✅ Key verified and activated!")
                    return True
                else:
                    print("⚠️ Failed to mark key as used.")
                    return True
        print("❌ Invalid key! Contact admin.")
        return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False

def key_gate():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🔑  MJ TOOL ACCESS REQUIRED 🔑\n")
    key = input("Enter your access key: ").strip()
    print("Checking key...")
    if not check_key_valid(key):
        time.sleep(1.5)
        exit()
    time.sleep(0.5)
# ===[ END KEY SYSTEM ADDITION ]===


# ===[ START OF YOUR ORIGINAL CODE — UNTOUCHED ]===
import requests
import json
import time
import os

try:
    from colorama import Fore, Style, init as colorama_init
    from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
except ImportError:
    print("Missing dependencies. Please install first:")
    print("  pip install colorama pystyle requests")
    exit()

colorama_init(autoreset=True)

# === UI / Styling (main.py style) ===
# =========[ Helper: show_progress (main.py style) ]=========
def show_progress(message="Loading...", duration=1.2):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN]
    symbols = ['•', '•', '•']
    left_bracket = Fore.BLUE + Style.BRIGHT + '⟨' + Style.RESET_ALL
    right_bracket = Fore.BLUE + Style.BRIGHT + '⟩' + Style.RESET_ALL
    print(f"{Fore.CYAN}  ---[{Style.RESET_ALL}{message} ", end="")
    print(left_bracket, end="", flush=True)
    start_time = time.time()
    steps = 18
    delay = max(0.02, duration / steps)
    for i in range(steps):
        color = colors[i % len(colors)]
        symbol = color + symbols[i % len(symbols)] + Style.RESET_ALL
        print(symbol, end="", flush=True)
        time.sleep(delay)
    print(right_bracket + f" {Fore.GREEN}100%" + Style.RESET_ALL)
    print()

# =========[ Banner (main.py style) ]=========
_BANNER_ASCII = """
════════════════════════════════════════════════════
                                                  
      █▀▄▀█ ░░█ █▀▀ █▀█ █▀▄▀█ ▀█▀ █▀█ █▀█ █
      █░▀░█ █▄█ █▄▄ █▀▀ █░▀░█ ░█░ █▄█ █▄█ █▄▄                                          
════════════════════════════════════════════════════
  👑 MJCPMTOOL | Car Parking Multiplayer 1 & 2👑
════════════════════════════════════════════════════
"""

def splash():
    try:
        Anime.Fade(Center.Center(_BANNER_ASCII), Colors.yellow_to_red, Colorate.Vertical, enter=True)
    except Exception:
        print(_BANNER_ASCII)
        input("[ Press Enter to continue ]")
    System.Clear()
# ===[ INSERTED HERE: key gate runs AFTER splash ]===

def header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.green_to_white, "=" * 60))
    print(Colorate.Horizontal(Colors.red_to_yellow, "    𝗠𝗝 𝗖𝗣𝗠 𝗧𝗢𝗢𝗟  •  𝗖𝗔𝗥 𝗣𝗔𝗥𝗞𝗜𝗡𝗚 𝗠𝗨𝗟𝗧𝗜𝗣𝗟𝗔𝗬𝗘𝗥 𝟭 & 𝟮 "))
    print(Colorate.Horizontal(Colors.green_to_white, "=" * 60))
    print(f"{Fore.MAGENTA}< Logout your CPM account from game before using this tool! >{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Telegram: @MJ_GARAGE\n")


# --- Game Configurations ---
GAMES = {
    "1": {
        "name": "Car Parking Multiplayer",
        "firebase_api_key": os.environ.get("CPM1_API_KEY", "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM"),
        "rank_url": os.environ.get("CPM1_RANK_URL", "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"),
        "login_tag": "Cpm1"
    },
    "2": {
        "name": "Car Parking Multiplayer 2",
        "firebase_api_key": os.environ.get("CPM2_API_KEY", "AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ"),
        "rank_url": os.environ.get("CPM2_RANK_URL", "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SetUserRating17_AppI"),
        "login_tag": "Cpm2"
    }
}

# Initialize Firebase Admin SDK (Do this ONCE at the start of your program)
try:
    import firebase_admin
    from firebase_admin import credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized using environment variables.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
except ImportError:
    print("Firebase Admin SDK is not installed. Please install it using: pip install firebase_admin")

def login(email, password, game):
    print(f"\n🔐 Logging in to {game['name']}...")
    login_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={game['firebase_api_key']}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12)", "Content-Type": "application/json"}
    try:
        response = requests.post(login_url, headers=headers, json=payload)
        response_data = response.json()
        if response.status_code == 200 and 'idToken' in response_data:
            print("✅ Login successful!")
            return response_data.get('idToken')
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error during login.")
            print(f"❌ Login failed: {error_message}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None

# ===[ key check runs here after splash ]===
def main():
    splash()  # Show splash first
    key_gate()  # Then ask for key
    # Continue normal logic
    while True:
        header()
        print(Colorate.Horizontal(Colors.blue_to_cyan, "Select Game Version:"))
        print(f"{Fore.GREEN}1. Car Parking Multiplayer 1{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. Car Parking Multiplayer 2{Style.RESET_ALL}")
        print(f"{Fore.RED}0. Exit{Style.RESET_ALL}")
        choice = input("Enter choice: ").strip()
        if choice == "0":
            print("Exiting...")
            break
        elif choice in GAMES:
            game = GAMES[choice]
            print(f"\nSelected {Colorate.Horizontal(Colors.blue_to_cyan, game['name'])}")
            try:
                email = input("📧 Enter email: ").strip()
                password = input("🔒 Enter password: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break
            token = login(email, password, game)
            if token:
                # original continues...
                pass
        else:
            print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()

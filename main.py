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

# ======== [ 🔑 KEY SYSTEM ADDED HERE - NO REMOVALS ] ========
KEY_SERVER = "https://mjpanel.42web.io/api.php"  # <- CHANGE THIS to your PHP endpoint

def verify_key(user_key):
    try:
        response = requests.post(KEY_SERVER, data={"key": user_key, "action": "verify"})
        # Expecting JSON like: {"valid": true} or {"valid": false}
        data = response.json()
        return data.get("valid", False)
    except Exception as e:
        print(f"❌ Error checking key: {e}")
        return False
# ============================================================


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
    # Fancy fade splash
    try:
        Anime.Fade(Center.Center(_BANNER_ASCII), Colors.yellow_to_red, Colorate.Vertical, enter=True)
    except Exception:
        # If Anime fails (headless), fallback to simple print
        print(_BANNER_ASCII)
        input("[ Press Enter to continue ]")
    System.Clear()

def header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.green_to_white, "=" * 60))
    print(Colorate.Horizontal(Colors.red_to_yellow, "    𝗠𝗝 𝗖𝗣𝗠 𝗧𝗢𝗢𝗟  •  𝗖𝗔𝗥 𝗣𝗔𝗥𝗞𝗜𝗡𝗚 𝗠𝗨𝗟𝗧𝗜𝗣𝗔𝗬𝗘𝗥 𝟭 & 𝟮 "))
    print(Colorate.Horizontal(Colors.green_to_white, "=" * 60))
    print(f"{Fore.MAGENTA}< Logout your CPM account from game before using this tool! >{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Telegram: @MJ_GARAGE\n")


# --- Game Configurations ---
GAMES = {
    "1": {
              "name": "Car Parking Multiplayer",
        "firebase_api_key": os.environ.get("CPM1_API_KEY", "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM"),  # Use environment variable
        "rank_url": os.environ.get("CPM1_RANK_URL", "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"),  # Use environment variable
        "login_tag": "Cpm1"
    },
    "2": {
        "name": "Car Parking Multiplayer 2",
        "firebase_api_key": os.environ.get("CPM2_API_KEY", "AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ"),  # Use environment variable
        "rank_url": os.environ.get("CPM2_RANK_URL", "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SetUserRating17_AppI"),  # Use environment variable
        "login_tag": "Cpm2"
    }
}

# Initialize Firebase Admin SDK (Do this ONCE at the start of your program)
try:
    import firebase_admin
    from firebase_admin import credentials
    cred = credentials.ApplicationDefault()  # Use environment variable for credentials
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized using environment variables.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    # Optionally, exit if Firebase is critical
    # exit()
except ImportError:
    print("Firebase Admin SDK is not installed. Please install it using: pip install firebase_admin")

def login(email, password, game):
    print(f"\n🔐 Logging in to {game['name']}...")
    login_url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={game['firebase_api_key']}" # Fixed URL
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12)",
        "Content-Type": "application/json"
    }
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

def set_rank(token, game):
    print("👑 Injecting KING RANK...")
    rating_data = {k: 100000 for k in [
        "cars", "car_fix", "car_collided", "car_exchange", "car_trade", "car_wash",
        "slicer_cut", "drift_max", "drift", "cargo", "delivery", "taxi", "levels", "gifts",
        "fuel", "offroad", "speed_banner", "reactions", "police", "run", "real_estate",
        "t_distance", "treasure", "block_post", "push_ups", "burnt_tire", "passanger_distance"
    ]}
    rating_data["time"] = 10000000000
    rating_data["race_win"] = 3000
    payload = {"data": json.dumps({"RatingData": rating_data})}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }
    try:
        response = requests.post(game["rank_url"], headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ Rank successfully set!")
            return True
        else:
            print(f"❌ Failed to set rank. HTTP Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error during rank set: {e}")
        return False

def change_password(token, game, new_password):
    print("🔐 Changing password...")
    change_password_url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={game['firebase_api_key']}"  # fixed URL
    payload = {
        "idToken": token,
        "password": new_password,
        "returnSecureToken": True
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(change_password_url, headers=headers, json=payload)
        response_data = response.json()
        if response.status_code == 200:
            print("✅ Password changed successfully!")
            return True
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error during password change.")
            print(f"❌ Password change failed: {error_message}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error during password change: {e}")
        return False

def change_email(token, game, new_email):
    print("📧 Changing email...")
    change_email_url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={game['firebase_api_key']}" # Fixed URL
    payload = {
        "idToken": token,
        "email": new_email,
        "returnSecureToken": True
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(change_email_url, headers=headers, json=payload)
        response_data = response.json()
        if response.status_code == 200 and 'email' in response_data:
            print("✅ Email changed successfully!")
            return response_data['email']  # return the new email
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error during email change.")
            print(f"❌ Email change failed: {error_message}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error during email change: {e}")
        return None

def game_menu(token, game):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen before displaying the menu
        print(f"\n{Colorate.Horizontal(Colors.blue_to_cyan, game['name'])} - Select an action:")
        print(f"{Fore.YELLOW}1. KING RANK{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. CHANGE GMAIL{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. CHANGE PASS{Style.RESET_ALL}")
        print(f"{Fore.RED}0. Back to game selection{Style.RESET_ALL}")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            show_progress("Setting King Rank...")
            set_rank(token, game)
            input("Press Enter to continue...")  # Wait for user to acknowledge
        elif choice == "2":
            new_email = input("Enter new email: ").strip()
            show_progress("Changing Gmail...")
            new_email_address = change_email(token, game, new_email)  # get the new email
            if new_email_address:
                print(f"Email changed successfully to: {new_email_address}")
            else:
                print("Failed to change email.")
            input("Press Enter to continue...")  # Wait for user to acknowledge
        elif choice == "3":
            new_password = input("Enter new password: ").strip()
            show_progress("Changing Password...")
            if change_password(token, game, new_password):
                print("Password changed successfully.")
            else:
                print("Failed to change password.")
            input("Press Enter to continue...")  # Wait for user to acknowledge
        elif choice == "0":
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice.{Style.RESET_ALL}")
            input("Press Enter to continue...")  # Wait for user to acknowledge

def main():
    splash()  # Display the splash screen

    # ======== [ KEY SYSTEM PROMPT - ADDED HERE, NO REMOVALS ] ========
    try:
        print(Colorate.Horizontal(Colors.red_to_yellow, "🔑 ENTER YOUR ACCESS KEY TO CONTINUE"))
    except Exception:
        # If Colorate fails for any reason, still print a basic prompt
        print("🔑 ENTER YOUR ACCESS KEY TO CONTINUE")
    user_key = input("Enter your key: ").strip()
    print("\nChecking key validity...\n")
    if not verify_key(user_key):
        print(f"{Fore.RED}❌ Invalid or expired key. Please contact admin.{Style.RESET_ALL}")
        input("Press Enter to exit...")
        return
    print(f"{Fore.GREEN}✅ Key verified! Access granted.{Style.RESET_ALL}")
    time.sleep(1)
    # ===============================================================

    while True:
        header()  # Display the header
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
                game_menu(token, game)
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please select 1, 2, or 0.{Style.RESET_ALL}")
            input("Press Enter to continue...")  # Wait for user to acknowledge

if __name__ == "__main__":
    main()

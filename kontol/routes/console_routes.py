import json
import paramiko
import threading
from flask import Blueprint, jsonify, request

Console = Blueprint("Console", __name__)

@Console.route("/console", methods=["GET"])
def add_proxy_admin():
    admin_key = request.args.get('key')
    inputs = request.args.get('input')
    
    if not all([admin_key, inputs]):
        return jsonify({"result": "Enter correctly"}), 400
    
    with open("./data/admin.json") as e:
        admkey = json.load(e)
    
    with open("./data/vps_servers.json") as file:
        ssh_servers = json.load(file)

    if admin_key not in admkey['keys']:
        return jsonify({"error": "Key invalid"}), 400
        
    def connect_to_ssh_server(server):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(server['hostname'], port=server['port'], username=server['username'], password=server['password'])
        except paramiko.AuthenticationException:
            print(f"Failed to connect to {server['hostname']} - Authentication failed")
            return False
        except paramiko.SSHException as e:
            print(f"Failed to connect to {server['hostname']} - {str(e)}")
            return False
        except Exception as e:
            print(f"Error connecting to {server['hostname']} - {str(e)}")
            return False
            
        command = f"{inputs}"
        print(f"{inputs}")
        
        stdin, stdout, stderr = ssh.exec_command(command)
        ssh.close()
        return True
    
    threads = []
    for server in ssh_servers:
        thread = threading.Thread(target=connect_to_ssh_server, args=(server,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    return jsonify({f"{inputs}"})
import json, datetime, re, requests, paramiko, threading
from flask import Blueprint, jsonify, request, render_template
from funcs.string import str_equals, is_str_empty, sanitize, str_validation

Admin = Blueprint("Admin", __name__)

@Admin.route("/admin/addkey", methods=["GET"])
def index_addkey():
  if 'adminkey' in request.args and 'keyname' in request.args and 'expired' in request.args and 'maxtime' in request.args and 'plans' in request.args and 'maxconc' in request.args:
    adminkey = sanitize(request.args.get('adminkey', default=None, type=str))
    keyname = sanitize(request.args.get('keyname', default=None, type=str))
    expired = sanitize(request.args.get('expired', default=None, type=str))
    maxtime = sanitize(request.args.get('maxtime', default=None, type=str))
    plans = sanitize(request.args.get('plans', default=None, type=str))
    maxcons = sanitize(request.args.get('maxconc', default=None, type=str))
  else:
    logs = "Missing argument(s)"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
    
  if not all([adminkey, keyname, expired, maxtime, plans, maxcons]):
    logs = "Missing argument(s)"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
        
  with open("./data/database.json") as e:
    db = json.load(e)
    
  with open("./data/admin_key.json") as e:
    admkey = json.load(e)

  if str_validation(adminkey):
      return jsonify({"response_message": "Error, Malcious character detected."})
  
  if str_validation(keyname):
      return jsonify({"response_message": "Error, Malcious character detected."})
  
  if str_validation(expired):
      return jsonify({"response_message": "Error, Malcious character detected."})
  
  if str_validation(maxtime):
      return jsonify({"response_message": "Error, Malcious character detected."})
  
  if str_validation(plans):
      return jsonify({"response_message": "Error, Malcious character detected."})
  
  if str_validation(maxcons):
      return jsonify({"response_message": "Error, Malcious character detected."})
  
  if not maxtime.isdigit():
      return jsonify({"response_message": "Maxtime must digit."})
  
  if not maxcons.isdigit():
      return jsonify({"response_message": "Maxconc must digit."})
  
  if not maxtime.isdigit():
      return jsonify({"response_message": "Curconc cmust digit."})
  
  if re.match(r'^\d{4}-\d{2}-\d{2}$', expired):
    logs = "Format must YEAR-MONTH-DAY, ex: 2045-12-2."
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
  else:
    expired = expired
      
  if adminkey not in admkey['keys']:
    logs = "Key invalid"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
    
  try:
    db["keys"][keyname] = {"exp": expired, "maxTime": maxtime, "plans": plans, "maxCons": maxcons}
    with open("./data/database.json", "w") as json_file:
      json.dump(db, json_file, indent=4)
    status = "✅ Successfully"
    data = f"Key: {keyname}\nExpired: {expired}\nMaxtime: {maxtime}\nPlans: {plans}\nMaxCons: {maxcons}"
    return render_template('admin.html', status=status, data=data)
  except Exception as e:
    return jsonify({"response_message": "An error occurred."})
    print(e)

@Admin.route("/admin/deletekey", methods=["GET"])
def index_deleted_key():
  if 'adminkey' in request.args and 'keyname' in request.args:
    adminkey = sanitize(request.args.get('adminkey', default=None, type=str))
    keyname = sanitize(request.args.get('keyname', default=None, type=str))
  else:
    logs = "Missing argument(s)"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
    
    
  if not all([adminkey, keyname]):
    logs = "Missing argument(s)"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
        
  with open("./data/database.json") as e:
    db = json.load(e)
    
  with open("./data/admin_key.json") as e:
    admkey = json.load(e)

  if str_validation(adminkey):
    return jsonify({"response_message": "Error, Malcious character detected."})
    
  if str_validation(keyname):
    return jsonify({"response_message": "Error, Malcious character detected."})

  if adminkey not in admkey['keys']:
    return jsonify({"response_message": "Key invalid."})
    
  try:
    del db["keys"][keyname]
    with open("./data/database.json", "w") as json_file:
      json.dump(db, json_file, indent=4)
    status = "✅ Successfully"
    data = f"Key: {keyname}\nData key deleted"
    return render_template('admin.html', status=status, data=data)
  except Exception as e:
    return jsonify({"response_message": "An error occurred."})
    print(e)
        
@Admin.route("/admin/addservers", methods=["GET"])
def index_add_server():
  if 'adminkey' in request.args and 'hostname' in request.args and 'username' in request.args and 'password' in request.args:
    adminkey = sanitize(request.args.get('adminkey', default=None, type=str))
    hostname = sanitize(request.args.get('hostname', default=None, type=str))
    username = sanitize(request.args.get('username', default=None, type=str))
    password = sanitize(request.args.get('password', default=None, type=str))
  else:
    logs = "Missing argument(s)"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
    
  if not all([adminkey, hostname, username, password]):
    logs = "Missing argument(s)"
    status = "❌ Not Found"
    return render_template('admin.html', logs=logs, status=status)
        
  with open("./data/vps_servers.json") as e:
    db = json.load(e)
  
  with open("./data/admin_key.json") as e:
    admkey = json.load(e)
    
  if str_validation(adminkey):
    return jsonify({"response_message": "Error, Malcious character detected."})
  
  if adminkey not in admkey['keys']:
    return jsonify({"response_message": "Key invalid."})
  
  try:
    db.append({"hostname": hostname, "username": username, "password": password})
    with open("./data/vps_servers.json", "w") as json_file:
      json.dump(db, json_file, indent=4)
    status = "✅ Successfully"
    data = f"Hostname: {hostname}\nUsername: {username}\nPassword: {password}"
    return render_template('admin.html', status=status, data=data)
  except Exception as e:
    return jsonify({"response_message": "An error occurred."})
    print(e)

@Admin.route("/admin/autoproxy", methods=["GET"])
def add_proxy_admin():
    admin_key = request.args.get('adminkey')
    
    # Load admin keys, VPS servers, and attack command from respective files
    with open("./data/admin.json") as e:
        admkey = json.load(e)
    
    with open("./data/vps_servers.json") as file:
        ssh_servers = json.load(file)
        
    with open("./data/attacks.json") as file:
        proxy_send = json.load(file)

    # Validate the admin key
    if admin_key not in admkey['keys']:
        return jsonify({"response_message": "Key invalid"}), 400

    # Ensure proxy_send is a string
    if isinstance(proxy_send, list):
        proxy_send = ' '.join(proxy_send)  # Convert list to string
    elif not isinstance(proxy_send, str):
        proxy_send = str(proxy_send)  # Convert anything else to string

    print(f"DEBUG: proxy_send type: {type(proxy_send)}")
    print(f"DEBUG: proxy_send content: {proxy_send}")

    # Function to connect to SSH server and send the command
    def connect_to_ssh_server(server):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(server['hostname'], port=server['port'], username=server['username'], password=server['password'])
            stdin, stdout, stderr = ssh.exec_command(proxy_send)
            ssh.close()
            return True
        except paramiko.AuthenticationException:
            print(f"Failed to connect to {server['hostname']} - Authentication failed")
        except paramiko.SSHException as e:
            print(f"Failed to connect to {server['hostname']} - {str(e)}")
        except Exception as e:
            print(f"Error connecting to {server['hostname']} - {str(e)}")
        return False

    # Pruning: keep only the servers that successfully connect
    ssh_servers = [server for server in ssh_servers if connect_to_ssh_server(server)]

    # Save the pruned list back to the JSON file
    with open("./data/vps_servers.json", "w") as file:
        json.dump(ssh_servers, file, indent=4)

    return jsonify({
        "result": {
            "Successfull Add": {
                "Wait until the process is complete."
            }
        }
    }), 200
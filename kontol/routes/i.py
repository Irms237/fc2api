from flask import render_template, Blueprint, request, jsonify
import json, datetime, time, threading
from urllib.parse import urlparse
from funcs.validator import Validation
from funcs.launch_attack import launch_attacks
from funcs.method_check import check_attack_method
from funcs.string import str_equals, is_str_empty, sanitize, str_validation
from apscheduler.schedulers.background import BackgroundScheduler
from funcs.blacklist import is_target_blacklisted, blacklisted_targets

Attack = Blueprint("Attack", __name__)

with open("./data/methods.json") as files:
  data_met = json.load(files)

scheduler = BackgroundScheduler()
attack_slots = 0
max_slots = 999
active_targets = {}
last_target_input = {}

layer7_methods = []
layer4_methods = []

for layer, methods in data_met['methods'].items():
    for type in methods:
        if layer == 'layer7':
            layer7_methods.extend(methods[type])
        elif layer == 'layer4':
            layer4_methods.extend(methods[type])

layer7_methods = list(set(method.upper() for method in layer7_methods))
layer4_methods = list(set(method.upper() for method in layer4_methods))

def read_blacklisted_targets():
  try:
    with open('./data/blacklist.txt', 'r') as f:
      lines = f.readlines()
      for line in lines:
        if line.strip():
          blacklisted_targets.add(line.strip())
  except FileNotFoundError:
      pass

@Attack.route("/api", methods=["GET"])
def index_flood():
    if 'key' in request.args and 'host' in request.args and 'port' in request.args and 'time' in request.args and 'method' in request.args:
        key = sanitize(request.args.get('key', default=None, type=str))
        host = sanitize(request.args.get('host', default=None, type=str))
        port = sanitize(request.args.get('port', default=None, type=str))
        times = sanitize(request.args.get('time', default=None, type=str))
        method = sanitize(request.args.get('method', default=None, type=str))
    else:
        logs = "Missing argument"
        status = "? Not Found" 
        return render_template('attack.html', logs=logs, status=status)
    
    global attack_slots
    if not all([key, host, port, times, method]):
        logs = "Null values."
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
    
    if not Validation.is_valid_key(key):
        logs = "Key Expired or not valid."
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
        
    with open("./data/database.json") as e:
        db = json.load(e)
        
    usrdata = db['keys'][key]
    max_cons = usrdata.get('maxCons')
    if attack_slots >= max_cons:
        logs = f"Your concurrents max is {max_cons}"
        status = "? Limited conc"
        return render_template('attack.html', logs=logs, status=status)

    if attack_slots > max_slots:
        logs = "Slots is full, please wait"
        status = "? Slot full"
        return render_template('attack.html', logs=logs, status=status)
        
    if method.upper() == "STOP":
        method = method
    else:
        if method.upper() not in layer7_methods and method.upper() not in layer4_methods and method.upper():
            logs = "Method invalid."
            status = "? Not Found"
            return render_template('attack.html', logs=logs, status=status)
        
    if str_validation(port):
        return jsonify({"system": "Error, Malcious character detected."})
    
    if str_validation(times):
        return jsonify({"system": "Error, Malcious character detected."})
    
    if str_validation(method):
        return jsonify({"system": "Error, Malicious character detected."})
        
    usrdata = db["keys"]
    if not usrdata.get(key):
        logs = "Key not valid"
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
        
    if is_target_blacklisted(host):
        logs = "Target is blacklisted by system."
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
        
    if not Validation.validate_ip(host):
        if not Validation.validate_url(host):
            logs = "Target is not an Ipv4 or an URL."
            status = "? Not Found"
            return render_template('attack.html', logs=logs, status=status)
        else:
            host = host
    else:
        host = host
    
    if not Validation.validate_port(port):
        logs = "Port should be in the range of (1-65535)."
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
        
    user_maxtime = db["keys"][key]["maxTime"]
    if not Validation.validate_time(key, times):
        logs = f"Time should be MIN=1, MAX={user_maxtime}."
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
    
    user_data = db["keys"].get(key)
    if user_data and user_data.get('plans') == "BASIC":
        allowed_methods = {
            "layer7": [m.upper() for m in data_met['methods']['layer7']['basic']],
            "layer4": [m.upper() for m in data_met['methods']['layer4']['basic']],
            "stop": data_met['methods']['stop']
        }
    else:
        allowed_methods = {
            "layer7": [m.upper() for m in method for method in data_met['methods']['layer7'].values()],
            "layer4": [m.upper() for m in method for method in data_met['methods']['layer4'].values()],
            "stop": data_met['methods']['stop']
        }
    
    def is_method_allowed(layer, method):
        return method.upper() in allowed_methods.get(layer, [])
    
    if method.upper() in layer4_methods:
        layer = "layer4"
    else:
        layer = "layer7"
   
    if not is_method_allowed(layer, method):
        logs = f"You cannot use VIP plans, methods={method.upper()}"
        status = "? Not Found"
        return render_template('attack.html', logs=logs, status=status)
    
    def remove_target(host):
        time.sleep(int(times))
        active_targets.pop(host, None)
      
    def decrease_slots():
        global attack_slots
        attack_slots -= 1
        print(f'slot decreased. Slots in use: {attack_slots}')
        
        if attack_slots == 0:
            scheduler.remove_all_jobs()
            print('All slots freed.')
        
    attack_slots += 1
    print(f'Attack started on {host}. Slots in use: {attack_slots}')
    
    print(f'Starting Attack, All Ongoing {attack_slots}')
    scheduler.add_job(decrease_slots, 'interval', seconds=int(times))
    
    last_target_input[host] = time.time()
    active_targets[host] = threading.Thread(target=remove_target, args=(host,))
    active_targets[host].start()
    
    start_time = time.time()
    launch_attacks(method, host, port, times)
    
    end_time = time.time()
    hasil = end_time - start_time
    delay = "{:.5f}".format(hasil)
    status = "? Good"
    slots = f"{attack_slots}/{max_slots}"
    return render_template('attack.html', status=status, host=host, port=port, times=times, method=method.upper(), delay=delay, slots=slots), 200

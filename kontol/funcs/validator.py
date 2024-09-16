import datetime
from datetime import datetime
import validators
import ipaddress
import json
from ipaddress import IPv4Address, IPv4Network

class Validation:
    @staticmethod
    def validate_ip(ip):
        parts = ip.split('.')
        return len(parts) == 4 and all(x.isdigit() for x in parts) and all(0 <= int(x) <= 255 for x in parts) and not ipaddress.ip_address(ip).is_private
    
    @staticmethod
    def validate_port(port, rand=False):
        if rand:
            return port.isdigit() and int(port) >= 0 and int(port) <= 65535
        else:
            return port.isdigit() and int(port) >= 1 and int(port) <= 65535

    @staticmethod
    def validate_time(key, times):
        with open("./data/database.json") as e:
            data = json.load(e)
        return times.isdigit() and int(times) >= 10 and int(times) <= data["keys"][key]["maxTime"]
    
    @staticmethod
    def validate_method(method):
        with open("./data/attacks.json") as e:
            data = json.load(e)
        for i in data:
          if i["methods"] == method.upper():
            return True
          else:
            return False
    
    @staticmethod
    def is_valid_key(key):
        with open("./data/database.json") as e:
            data = json.load(e)
        
        if key in data['keys']:
            key_data = data['keys'][key]
            if datetime.strptime(key_data['exp'], '%Y-%m-%d') >= datetime.now():
                return True
            else:
                return False
        else:
            return False
    
    @staticmethod
    def validate_domain(domain):
        return validators.domain(domain)

    @staticmethod
    def validate_url(url):
        return validators.url(url)

    @staticmethod
    def ip_list_blacklist(ip):
        with open("./data/blacklist.json") as e:
            data = json.load(e)
        list = data["hosts"]
        if ip in list:
            return True
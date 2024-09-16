import ipaddress
from urllib.parse import urlparse

blacklisted_targets = set()

def read_blacklisted_targets():
  try:
    with open('./data/blacklist.txt', 'r') as f:
      lines = f.readlines()
      for line in lines:
        if line.strip():
          blacklisted_targets.add(line.strip())
  except FileNotFoundError:
      pass

def is_ip_in_blacklist(ip_address):
    return ip_address in blacklisted_targets

def is_domain_in_blacklist(domain):
    return any(blacklisted_domain in domain for blacklisted_domain in blacklisted_targets)

def get_target_type(target):
    try:
        ipaddress.ip_address(target)
        return 'ip'
    except ValueError:
        return 'domain'

def get_domain_from_target(target):
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    parsed_url = urlparse(target)
    return parsed_url.netloc

def is_target_blacklisted(target):
    target_type = get_target_type(target)
    if target_type == 'domain':
        domain = get_domain_from_target(target)
        return is_domain_in_blacklist(domain)
    elif target_type == 'ip':
        return is_ip_in_blacklist(target)
    return False

read_blacklisted_targets()
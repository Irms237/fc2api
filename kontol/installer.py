# python3 installer.py
import os, time, sys

os.system('clear')
os.system('apt install python3-pip')
time.sleep(1)
os.system('python3 -m pip -r requirements.txt')
os.system('clear')
time.sleep(2)
os.system("screen python3 main.py")
sys.exit()
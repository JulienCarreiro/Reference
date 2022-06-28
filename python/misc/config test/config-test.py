#!/bin/python3
import configparser

parser = configparser.ConfigParser()
parser.read('conf.ini')

username = parser.get('Settings', 'Username')
homedir = parser.get('Settings', 'Home')
logfile = parser.get('Settings', 'Logfile')
server_addr = parser.get('Settings', 'Server')
ino_port = parser.get('Settings', 'Arduino')

print(username, homedir, logfile, server_addr, ino_port)
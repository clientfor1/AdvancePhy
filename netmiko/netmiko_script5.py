#!/usr/bin/python3
#(c) 2017 Todd Riemenschneider
#This script will allow up to update a group of hosts with common config shared by all
#Enable Multiprocessing 
from multiprocessing import Pool
#getpass will not display password
from getpass import getpass
#ConnectionHandler is the function used by netmiko to connect to devices
from netmiko import ConnectHandler
#Time tracker
from time import time

#create variables for username and password
#create variables for configs and hosts
uname = input("Username: ")
passwd = getpass("Password: ")
cmd = input("Enter config commands seperated by ',': ")
host = input("Enter the host IPs seperate with space: ")

#This will allow you to just press enter
#This sets default values Not recommanded in any place but a lab
if len(uname) < 1 : uname = "automate"
if len(passwd) < 1 : passwd = "automation"

#create lists of hosts and cmds to iterate through
#This list can contain show or config commands show commands require "do + command"
hosts = host.split()
cmds = cmd.split(",")

starting_time = time()

#Each member of the pool of 5 will be run through this function
def run_script(host_ip):
    ios_rtr = {
        "device_type": "cisco_ios",
        "ip": host_ip,
        "username": uname,
        "password": passwd,
        }
    #connect to the device via ssh
    net_connect = ConnectHandler(**ios_rtr)
    #print the device IP to identify which device is being configured
    print("Connected to host:", host_ip)
    #this variable is used to capture the output of cmds sent to device
    output = net_connect.send_config_set(cmds)
    #print the output
    print(output)
    print('\n---- Elapsed time=', time()-starting_time)

if __name__ == "__main__":
    # Pool(5) means 5 process / devices will be run at a time, until youve gone through the device list
    with Pool(5) as p:
        print(p.map(run_script, hosts))

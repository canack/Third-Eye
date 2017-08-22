#!/usr/bin/python

import argparse
import os

from kismetclient import Client as KismetClient
from kismetclient import handlers

##### ARGPARSE AREA BEGIN #####
parser = argparse.ArgumentParser(
        description='''Third-Eye is people finder.
        If target people ( actually target device ) is your nearest Third-Eye will alert you.'''
        )

#parser.add_argument('-t', help='Target MAC address', required=True)
parser.add_argument('-i', help='Interface for use', required=True)

args = parser.parse_args()

INTERFACE = args.i
#TARGET = args.t.upper()
##### ARGPARSE AREA END #####


##### COLOR AREA BEGIN #####

RED = "\033[31m"
BLUE = "\033[34m"
GREEN = "\033[32m"
WHITE = "\033[0m"

##### COLOR AREA END #####

address = ('127.0.0.1', 2501)

k = KismetClient(address)
k.register_handler('TRACKINFO', handlers.print_fields)

import time

log_file = open('logs','a+')

TARGETS = open("address").readlines()
target_list = {}

for i in TARGETS:
    if not i.startwith("#"):
        target_list[i.strip("\n").split(' ')[0]] = " ".join(i.strip().split()[1:])


def handle_ssid(client, bssid, channel, signal_dbm):
    signal = str(signal_dbm.strip('-')[0])
    for target_mac, target_name in target_list.iteritems():
        target_mac = target_mac.upper()
        if target_mac == bssid:
            today_time = '( ' + time.strftime("%d/%m/%Y - %H:%M:%S") + ' )'
            os.popen("espeak '" + target_name + " " + signal + "' -p 12 -s 160 ")
            print BLUE + target_mac, target_name, '[ Signal lv:',signal, '] ' + today_time + WHITE
            log_file.write(target_mac + ' ' + target_name + ' [ Signal lv: ' + signal + ' ] Time: '+ today_time + "\n")
            log_file.flush()
            break
           

k.register_handler('CLIENT', handle_ssid)

while True:
    k.listen()



    



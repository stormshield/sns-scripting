#!/usr/bin/env python3

"""
Script to list SNS alarms
"""

import sys
import getpass
from operator import itemgetter
import argparse

from stormshield.sns.sslclient import SSLClient

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--host", help="Appliance to connect", default=None)
parser.add_argument("-u", "--user", help="Username", default="admin")
parser.add_argument("-p", "--password", help="password", default=None)
args = parser.parse_args()

host = args.host
user = args.user
password = args.password

if host is None:
    host = input("Appliance ip address: ")
if password is None:
    password = getpass.getpass("Password: ")

# connect to the appliance
client = SSLClient(
    host=host, port=443,
    user=user, password=password,
    sslverifyhost=False)

def error(msg):
    global client

    print("ERROR: {}".format(msg))
    client.disconnect()
    sys.exit(1)

def command(cmd):
    global client

    response = client.send_command(cmd)
    if not response:
        error("command failed:\n{}".format(response.output))

    return response

data = []

# get system events ...
response = command("CONFIG SYSEVENT SHOW")
for line in response.data['EventLevel']:
    data.append(["system", line['id'], line['msg']])

# ... and alarms
response = command("CONFIG SECURITYINSPECTION CONFIG ALARM LIST index=0")
for line in response.data['Alarm']:
    data.append([line['context'], line['id'], line['msg']])

# natural sort by context:id
data.sort(key=lambda x:x[0] + "{:04d}".format(int(x[1])))

for line in data:
    print("{}:{} \"{}\"".format(line[0], line[1], line[2]))

client.disconnect()

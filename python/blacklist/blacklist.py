#!/usr/bin/env python3

"""
Script to manage the IP blacklist
"""

import sys
import getpass
import argparse
import logging
import coloredlogs

coloredlogs.install(level='INFO', fmt="%(asctime)s %(message)s")

from stormshield.sns.sslclient import SSLClient

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-h", "--host", help="Appliance to connect", default=None)
parser.add_argument("-u", "--user", help="Username", default="admin")
parser.add_argument("-p", "--password", help="password", default=None)
parser.add_argument("-t", "--timeout", help="Expiration time (in seconds) of the IP in the list", default=60)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-f", "--file", help="Text file with the IP addresses")
group.add_argument("-l", "--list", action="store_true", help="List current blackist")

args = parser.parse_args()

host = args.host
user = args.user
password = args.password
ipfile = args.file
timeout = args.timeout
show = args.list

logging.info("SNS blacklist tool")

if host is None:
    host = input("Appliance ip address: ")
if user is None:
    user = input("Appliance user login: ")
if password is None:
    password = getpass.getpass("Password: ")

if ipfile:
    # check and open the text file
    addresses = []
    with open(ipfile, "r") as fh:
        for line in fh.readlines():
            #TODO check ip format v4/v6
            addresses.append(line.strip())

    logging.info(f"File {ipfile}: {len(addresses)} ip addresses")

    credentials = "BASE,MON_WRITE,FILTER"

if show:
    credentials = "BASE,FILTER_READ"

# connect to the appliance
client = SSLClient(
    host=host, port=443,
    user=user, password=password,
    credentials=credentials, # ask for limited privileges
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
        logging.error(f"command failed: {cmd}\n{response.output}")

    return response

if ipfile:
    command("MODIFY MONITOR FORCE ON")
    for address in addresses:
        response = command(f"MONITOR ADDRESSLIST ADD type=blacklist Name1={address}  Timeout={timeout}")
        if not response:
            sys.exit(1)
    logging.info(f"{len(addresses)} IP addresses added to the blacklist")

if show:
    print(command("MONITOR ADDRESSLIST SHOW type=blacklist"))

client.disconnect()


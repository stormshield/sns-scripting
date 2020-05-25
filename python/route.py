#!/usr/bin/env python3

"""
This example show how to retrieve static routing from a SNS appliance.
"""

import getpass
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

# default router
defr = client.send_command("CONFIG NETWORK DEFAULTROUTE SHOW")
print("\n".join(defr.output.split("\n")[1:-1]) + "\n")

print("-- IPv4 --\n")

# get ipv4 static routes
sroutev4 = client.send_command("CONFIG NETWORK ROUTE SHOW")
print("\n".join(sroutev4.output.split("\n")[1:-1]) + "\n")

# get ipv4 reverse routes
rev4 = client.send_command("CONFIG NETWORK ROUTE REVERSE SHOW")
print("\n".join(rev4.output.split("\n")[1:-1]) + "\n")

# get ipv4 multicast routing
mcast = client.send_command("CONFIG SMCROUTING ROUTE SHOW")
print("\n".join(mcast.output.split("\n")[1:-1]) + "\n")

print("-- IPv6 --\n")

# get ipv6 static routes
sroutev6 = client.send_command("CONFIG NETWORK ROUTE IPV6 SHOW")
print("\n".join(sroutev6.output.split("\n")[1:-1]) + "\n")

# get ipv6 reverse routes
rev6 = client.send_command("CONFIG NETWORK ROUTE IPV6 REVERSE SHOW")
print("\n".join(rev6.output.split("\n")[1:-1]) + "\n")

client.disconnect()

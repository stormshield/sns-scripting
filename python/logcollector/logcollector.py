#!/usr/bin/env python3

"""
Script to collect SNS logs
"""

# TODO
# check no double in logs
# get logger from lib
# multi-utm with a section for each utm in the ini

import sys
import logging
import os
import re
import logging
import coloredlogs
import configparser
from signal import signal, SIGINT

from stormshield.sns.sslclient import SSLClient

config = configparser.ConfigParser()
config.read("logcollector.ini")


# user input
host = config.get("Config", "host")
user = config.get("Config", "user")
password = config.get("Config", "password")

LIMIT = config.getint("Config", "limit")
LOG_DIR = config.get("Config", "log_dir")

last = configparser.ConfigParser()
last.read("last.ini")

logtypes = last.sections()
last_dates = {}

for logtype in logtypes:
    last_dates[logtype] = { "time": last.get(logtype, "time"), "tz": last.get(logtype, "tz")}

def writelast():
    global last_dates

    for logtype in logtypes:
        last.set(logtype, "time", last_dates[logtype]["time"])
        last.set(logtype, "tz", last_dates[logtype]["tz"])
    
    with open('last.ini', 'w') as cf:
        last.write(cf)

def handler(signal, frame):
    logger.info('SIGINT or CTRL-C detected. Exiting gracefully')
    writelast()
    exit(0)

signal(SIGINT, handler)

def writelog(logtype, msg):
    global last_dates, logger
    # get date
    search = re.search('time="(.*?) (.*?)" fw="(.*?)" tz=(.*?) ', msg)
    if not search:
        logger.warning("Can't extract date from the log")
        logger.debug(msg)
        return
    date = search.group(1)
    time = search.group(2)
    fw = search.group(3)
    tz = search.group(4)
    filename = fw + "_" + logtype + "_" + date + ".log"
    with open(os.path.join(LOG_DIR, filename), "a") as fh:
        fh.write(msg + "\n")
    last_dates[logtype]["time"] = date + " " + time
    last_dates[logtype]["tz"] = tz


logger = logging.Logger("logcollector")

coloredlogs.install(level='DEBUG', logger=logger, 
    fmt='%(asctime)s %(levelname)s %(message)s',
    field_styles={'asctime': {'color': 'black'}, 'levelname': { 'bold': True, 'color': 'blue'}})


# connect to the appliance
client = SSLClient(
    host=host, port=443,
    user=user, password=password,
    sslverifyhost=False)

# request ticket to be able to get the logs
response = client.send_command("SYSTEM RIGHT TICKET ACQUIRE")
if not response:
    logger.error("Can't get log ticket")
    logger.error(response.output)
    sys.exit(1)

for logtype in logtypes:
    count = 0
    while "log available":
        time = last_dates[logtype]["time"]
        tz = last_dates[logtype]["tz"]
        cmd = "LOG DOWNLIMIT name={logtype} first=\"{time}\" tz={tz} number={limit}".format(
            logtype=logtype, time=time, tz=tz, limit=LIMIT)
        logger.info("Getting log {} chunk from {} tz {}".format(logtype, time, tz))
        response = client.send_command(cmd)
        if not response:
            logger.error("Can't download {} log".format(logtype))
            logger.debug(cmd)
            logger.error(response.output)
            continue
        # first line is file name, second line is format
        for i in range(2, len(response.data["Result"])):
            count += 1
            writelog(logtype, response.data["Result"][i])

        if len(response.data["Result"]) < LIMIT + 2:
            logger.info("Info log {} downloaded ({} lines)".format(logtype, count))
            break


client.disconnect()

writelast()


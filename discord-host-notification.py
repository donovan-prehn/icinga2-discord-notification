#!/usr/bin/env python3
import socket
import requests
import argparse
import json
from datetime import datetime
parser = argparse.ArgumentParser(description='posts to discord webhook')

#Required
parser.add_argument('-d','--longdatetime', required=True)
parser.add_argument('-l','--hostname',  required=True)
parser.add_argument('-n', '--hostdisplayname', required=True)
parser.add_argument('-o', '--hostoutput', required=True)
parser.add_argument('-r', '--webhook', required=True)
parser.add_argument('-s', '--hoststate', required=True)
parser.add_argument('-t', '--notificationtype', required=True)

parser.add_argument('-4', help='HOSTADDRESS')
parser.add_argument('-6', help='HOSTADDRESS6')
parser.add_argument('-b', help='NOTIFICATIONAUTHORNAME')
parser.add_argument('-c', help='NOTIFICATIONCOMMENT')
parser.add_argument('-i', help='ICINGAWEB2URL')
parser.add_argument('-f', help='MAILFROM')
parser.add_argument('-v', help='HOSTADDRESS')

args = parser.parse_args()

title  = "[{}] {} is {}!".format(args.notificationtype, args.hostdisplayname, args.hoststate)
description = args.hostoutput
if args.c:
	description += '\n' + args.c

colcodes = {
    'UP' : '65280',
    'DOWN' :'16711680',
}
color = colcodes[args.hoststate]
datetime_object = datetime.strptime(args.longdatetime, '%Y-%m-%d %H:%M:%S %z')
timestamp  = datetime_object.strftime('%Y-%m-%dT%H:%M:%S.000%z')

url = args.webhook
embeds = []
alert = {
    "title" : title,
    'description' : description,
    "color" : color,
    'timestamp' : timestamp
}
embeds.append(alert)
if args.b:
	username = args.b
else:
	username = "Icinga"
payload = {"username" : username, 'embeds' : embeds}

r = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
print(r.status_code)

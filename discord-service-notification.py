#!/usr/bin/env python3
import socket
import requests
import argparse
import json
from datetime import datetime

colcodes = {
    'OK' : '65280',
    'WARNING' :'16776960',
    'CRITICAL' :'16711680',
    'UNKNOWN' : '6826080'
}

parser = argparse.ArgumentParser(description='posts to discord webhook')
# Required
parser.add_argument('-d','--longdatetime', help='LONGDATETIME ($icinga.long_date_time$)', required=True)
parser.add_argument('-e','--servicename', help='SERVICENAME ($icinga.long_date_time$)', required=True)
parser.add_argument('-l','--hostname', help='HOSTNAME ($icinga.long_date_time$)', required=True)
parser.add_argument('-n', '--hostdisplayname', help='HOSTDISPLAYNAME ($icinga.long_date_time$)', required=True)
parser.add_argument('-o', '--serviceoutput',help='SERVICEOUTPUT ($icinga.long_date_time$)', required=True)
parser.add_argument('-r', '--webhook', help='USEREMAIL ($icinga.long_date_time$)', required=True)
parser.add_argument('-s', '--servicestate', help='SERVICESTATE ($icinga.long_date_time$)', required=True)
parser.add_argument('-t', '--notificationtype', help='NOTIFICATIONTYPE ($icinga.long_date_time$)', required=True)
parser.add_argument('-u', '--servicedisplayname', help='SERVICEDISPLAYNAME ($icinga.long_date_time$)', required=True)

# Optional
parser.add_argument('-4', help='HOSTADDRESS')
parser.add_argument('-6', help='HOSTADDRESS6')
parser.add_argument('-b', help='NOTIFICATIONAUTHORNAME')
parser.add_argument('-c', help='NOTIFICATIONCOMMENT')
parser.add_argument('-i', help='ICINGAWEB2URL')
parser.add_argument('-f', help='MAILFROM')
parser.add_argument('-v', help='HOSTADDRESS')

args = parser.parse_args()

subject = "[{}] {} on {} is {}!".format(args.notificationtype, args.servicedisplayname, args.hostdisplayname, args.servicestate)
description = args.serviceoutput

datetime_object = datetime.strptime(args.longdatetime, '%Y-%m-%d %H:%M:%S %z')
newtime = datetime_object.strftime('%Y-%m-%dT%H:%M:%S.000%z')

alert = {
    "title" : subject,
    'description' : description,
    "color" : colcodes[args.servicestate],
    'timestamp' : newtime
}

embeds = []
embeds.append(alert)

# Send Notification
payload = {"username" : "Icinga", 'embeds' : embeds}
url = args.webhook
r = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

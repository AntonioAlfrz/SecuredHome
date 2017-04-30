import ConfigParser

import requests
import json

# Key server
Config = ConfigParser.ConfigParser()
Config.read("creds.ini")
section = "Firebase"
key = Config.get(section,"authorization_key")

# Mi movil
section = "Devices"
token = Config.get(section,"device1")
url = 'https://fcm.googleapis.com/fcm/send'
headers = {'Authorization': key,
           'Content-Type': 'application/json'
           }

def send_notification(to,title,text):
    payload = {
        'to': to,
        "notification": {
            "title": title,
            "text": text
        }
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print "Notification sent. Result: " + r.text

def send_data(to, data):
    payload = {
        'to': to,
        'data': data
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print "Data sent. Resul: " + r.text

# Prueba
# print "Executing Firebase Notification test"
# send_notification(token, "Notification from Python", "Mytext")

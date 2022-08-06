#!/usr/bin/python3
import requests
import json
import os
import os.path
from dotenv import load_dotenv

load_dotenv()

#CLE
#weatherStation="OHC093"
weatherStation=os.getenv('WEATHER_STATION')
msg = "No Warnings"
URL="https://api.weather.gov/alerts/active?zone={}".format(weatherStation)
aFile = "activeAlerts.dat"
pageId = os.getenv('FB_PAGE_ID') 
pageAccessToken = os.getenv('FB_PAGE_ACCESS_TOKEN')
fbURL = "https://graph.facebook.com/{}/feed?message={}&access_token={}"
header = {
        'User-Agent': 'LorainCountyWeatherBot',
        'From': 'mabeatty1978@gmail.com'
    }
#Read the current active alerts, if none, instatiate Alerts
if os.path.isfile(aFile):
    with open(aFile,"r") as temp_file:
        Alerts = [line.rstrip('\n') for line in temp_file]
else:
    Alerts = []

#Get the json from NWS
r = requests.get(URL, headers=header)
r_data = r.json()

if not r_data['features']:
    #There are no active alerts, delete active alert file
    if os.path.isfile(aFile):
        os.remove(aFile)
    exit()

for i, alert in enumerate(r_data['features']):
    headline = r_data['features'][i]['properties']['headline']
    description = r_data['features'][i]['properties']['description']
    instruction = r_data['features'][i]['properties']['instruction']
    alertId = r_data['features'][i]['id']
    
    #If the current alert is not in the existing list, don't send it
    #We only want to send new alerts
    if not alertId in Alerts:
        msg = headline + "\n\n" + description + "\n\n" + instruction
        a = open(aFile,"a")
        a.write(alertId + "\n")
        a.close()
        response = requests.post(fbURL.format(pageId, msg, pageAccessToken))
        d = response.json()
    i += 1


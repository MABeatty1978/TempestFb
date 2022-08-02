#!/usr/bin/python3
import requests
import json
import os
import os.path
from dotenv import load_dotenv
import tweepy

load_dotenv()

#CLE
#weatherStation="OHC093"
weatherStation=os.getenv('WEATHER_STATION')
consumer_key = os.getenv('TW_API_KEY')
consumer_secret = os.getenv('TW_API_KEY_SECRET')
access_token = os.getenv('TW_ACCESS_TOKEN')
access_token_secret = os.getenv('TW_ACCESS_TOKEN_SECRET')

msg = "No Warnings"
URL="https://api.weather.gov/alerts/active?point=41.45937174758735,-82.05589175178562"
aFile = "activeAlerts.dat"
pageId = os.getenv('FB_PAGE_ID') 
pageAccessToken = os.getenv('FB_PAGE_ACCESS_TOKEN')
fbURL = "https://graph.facebook.com/{}/feed?message={}&access_token={}"
header = {
        'User-Agent': 'LorainCountyWeatherBot',
        'From': 'mabeatty1978@gmail.com'
    }

wcAlertOffURL = "https://graph.api.smartthings.com/api/token/cb7539ee-020e-4f68-b288-5192fd2b5690/smartapps/installations/3a48394b-0361-4325-a378-73e7551c1bf4/execute/:8d3e905080f185eb19b504c29a4c1418:"
wcAlertOnURL = "https://graph.api.smartthings.com/api/token/cb7539ee-020e-4f68-b288-5192fd2b5690/smartapps/installations/3a48394b-0361-4325-a378-73e7551c1bf4/execute/:bf8d5fdbaf20e89b0ec41d10b0b539e2:"
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
        requests.post(wcAlertOffURL)
    exit()

for i, alert in enumerate(r_data['features']):
    headline = r_data['features'][i]['properties']['headline']
    description = r_data['features'][i]['properties']['description']
    instruction = r_data['features'][i]['properties']['instruction']
    alertId = r_data['features'][i]['id']
    
    #If the current alert is not in the existing list, don't send it
    #We only want to send new alerts
    if not alertId in Alerts:
        requests.post(wcAlertOnURL)
        msg = headline + "\n\n" + description + "\n\n" + instruction
        a = open(aFile,"a")
        a.write(alertId + "\n")
        a.close()
        #send to Facebook
        response = requests.post(fbURL.format(pageId, msg, pageAccessToken))
        d = response.json()
        #send to Twitter
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(headline)
    i += 1


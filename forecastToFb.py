#!/usr/bin/python3

import requests
import datetime
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

#Variable declarations
pageId = os.getenv('FB_PAGE_ID') 
pageAccessToken = os.getenv('FB_PAGE_ACCESS_TOKEN')
stationID = os.getenv('WF_STATION_ID')
tempestToken = os.getenv('WF_TOKEN')
tempestURL = "https://swd.weatherflow.com/swd/rest/better_forecast?station_id={}&units_temp=f&units_wind=mph&units_pressure=inhg&units_precip=in&units_distance=mi&token={}".format(stationID, tempestToken)
fbURL = "https://graph.facebook.com/{}/feed?message={}&access_token={}"
isToday = 0

#If the current time is after 6pm, get tomorrows forecast instead of today
t = datetime.datetime.now().strftime("%H")
if int(t) > 18:
    isToday = 1    

#Make the request to WeatherFlow to get the current day's forecast
#The third element of the response [0] represents the current day.  You can change this value to go further out, 1 = tomorrow etc.
r = requests.get(tempestURL)
data = r.json()
conditions = data['forecast']['daily'][isToday]['conditions']
sunrise = data['forecast']['daily'][isToday]['sunrise']
sunset = data['forecast']['daily'][isToday]['sunset']
highTemp = data['forecast']['daily'][isToday]['air_temp_high']
lowTemp = data['forecast']['daily'][isToday]['air_temp_low']
precipProb = data['forecast']['daily'][isToday]['precip_probability']
if precipProb !=0:
    precipType = data['forecast']['daily'][isToday]['precip_type']

highTemp = str(int(highTemp)) + u'\N{DEGREE SIGN}'
lowTemp = str(int(lowTemp)) + u'\N{DEGREE SIGN}'

#Format the sunrise/sunset epochs to be human friendly
sunset = datetime.datetime.fromtimestamp(sunset)
sunrise = datetime.datetime.fromtimestamp(sunrise)
sunset = sunset.strftime("%I:%M %p")        
sunrise = sunrise.strftime("%I:%M %p")

#Construct your message to send
if isToday == 0:
    msg = "Good Morning Lorain County!\n\nToday's "  
else:
    msg = "Good Evening Lorain County!\n\nTomorrow's "

msg = msg + "forecast is {}\nThe high will be {} and the low will be {}\n".format(conditions, highTemp, lowTemp)


if precipProb != 0:
    msg = msg + "The chance of {} is {} percent\n".format(precipType, precipProb)
else:
    msg = msg + "There is a 0 percent chance of precipitation\n"
msg = msg + "Sunrise is at {}, sunset will be at {}".format(sunrise, sunset)

#Send the message to your Facebook page
#If successful, the response will be formated with an 'id' for the post.  Otherwise, there will be an error message
response = requests.post(fbURL.format(pageId, msg, pageAccessToken))
d = response.json()


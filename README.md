# TempestFb
Sends a post to a Facebook Page with data collected from Tempest Weatherflow.  Word of warning, I wrote the following steps mostly from memory with some commands copy/pasted from Facebook documentation.  There may be some mistakes, please let me know if there are.

## Create a Facebook Page
https://www.facebook.com/help/104002523024878

## Create a Facebook App
https://developers.facebook.com/apps/
Type Business is what I chose, I don't see why None or even consumer wouldn't work
Once the app is created go into the basic settings on the left panel and note your AppID and AppSecret

## Get your Facebook access tokens.
This is the part I struggled witht the most to figure out.  If you plan on diving into Facebook app development more, I would strongly encourage to to spend some time and learn about how this part of the process works.  If you don't care and just want to make it work:
From the Facebook Developer Tools page https://developers.facebook.com/tools/ graph API explorer.  This explorer allows you to test http messages and see how data flows.  The page should load with me?fields=id,name in the explorer bar.  No need to do anything here, just click Submit".  You'll get a json response with your user id, copy this and save it, you'll need it later.
In the right panel, set the Facebook App field to the App you created.  For User or Page, you want User Token.  For permissions select pages_show_list, pages_read_engagement, pages_manage_metadata, pages_read_user_content, pages_manage_posts, pages_manage_engagement.
Click on Generate Access Token, this will give you your "short-lived-access-token", it's valid for 1 hour.
You need to use this access token to generate a long-lived-access-token.  To generate this token, open up a command shell and run:
curl -i -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&
  client_id=APP-ID&
  client_secret=APP-SECRET&
  fb_exchange_token=SHORT-LIVED-USER-ACCESS-TOKEN"
Replacing the APP-ID, APP-SECRET, and S-L-A-T with the values you collected in previous steps.
The resonse will contain your long-lived-access-token, save this value.
Now get your Page Access token.  To do this you'll need your Page ID.  You can get that from a few different places, but since you're already in the shell, you can run:
curl -i -X GET "https://graph.facebook.com/{user-id}/accounts
     ?access_token={user-access-token}"
replacing the user-id and user-access-tokens you collected from earlier.  The response will have the page's "id" in it.  To get the page access token:
curl -i -X GET "https://graph.facebook.com/PAGE-ID?
  fields=access_token&
  access_token=USER-ACCESS-TOKEN"
Replacing the USER-ACCESS-TOKEN with the long lived token you got earlier.  You can use the short lived, but it'll only generate a page access token that lives for an hour.  A page access token that is created with the long lived has no expiration date.  The response to this will have the page access token in it.  This page access token will go into your code.
Facebook access token documentation is here https://developers.facebook.com/docs/pages/getting-started

## Get your Tempest WeatherFlow Access Token and Station ID
Log into your account on tempestwx.com, go to Settings -> Data Authorizations -> Create Token.... copy this token down
Tempest API documentation is here https://weatherflow.github.io/Tempest/api/
Few different ways to get your Station ID, since you're already logged into the Tempest website, just click on the icon of the Tempest sensor in the top right, scroll down to the bottom and on the right there should be a little green dot next to Online.  Click the Online.

## Configure the python app
In the forecastToFb.py program set the values for myStationID and myPageToken appropriately.  




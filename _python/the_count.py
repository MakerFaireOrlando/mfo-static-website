import sys
import yaml
import unicodedata
import os
import os.path
import urllib
import time
import getopt
import requests
import os.path
from os import path
import imgflip

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

#define global variables
imgflipUser = ''
imgflipPass = ''
slackToken = ''
eventID = ''


def slackPermissionTroubleshooting():
    #Helpful code for troubleshooting channel permissions
    #permissions check, let's list private channels for this user
    try:
        # List all channels (public and private if scopes allow)
        #result = client.conversations_list(types="public_channel,private_channel")
        result = client.conversations_list(types="private_channel")
        for channel in result["channels"]:
            print(f"Name: {channel['name']}, ID: {channel['id']}, Is Private: {channel['is_private']}")
    except SlackApiError as e:
        print(f"Error fetching channels: {e.response['error']}")
        if e.response["error"] == "missing_scope":
            print(e.response["needed"]) #this will tell us a missing permission scope 

            
def postToSlack():

    global slackToken
    print("slackToken:" , slackToken)
    # Initialize Slack client
    client = WebClient(token=slackToken)
   
    # Upload the image to Slack
    try:
        response = client.files_upload_v2(
            channel="GBRHL2CUQ", #for private channels, you have to use the channel ID 
                                    #which you get from the url in the web version
                                    #also - be careful, some syntax shows this as channels=
                                    #lost over an hour on that one :(
            file="temp_image.jpg",
            title="Update"
            #,request_file_info = False
        )
        print("Image uploaded successfully:", response["file"]["permalink"])
    except SlackApiError as e:
        print("Error uploading file:", e.response["error"])
        print(e.response)
        if e.response["error"] == "missing_scope":
            print(e.response["needed"]) #this will tell us a missing permission scope 
  


def createImage(tix):

    print("createImage")

    # Meme details
    template_id = '15865071'  # Template ID for "The-Count"
    top_text = f"{tix} Tickets"
    bottom_text = "Ha! Ha! Ha!"

    # Imgflip API endpoint
    imgflip_url = "https://api.imgflip.com/caption_image"

    # Create meme
    payload = {
        'template_id': template_id,
        'username': imgflipUser,
        'password': imgflipPass,
        'text0': top_text,
        'text1': bottom_text
    }

    response = requests.post(imgflip_url, data=payload)
    print(response)

    img_result = response.json()
    print(img_result)

    if img_result['success']:
        meme_url = img_result['data']['url']
        print("Meme created successfully!")
        print("Meme URL:", meme_url)

         # Download the image
        response = requests.get(meme_url)
        if response.status_code == 200:
            print("Saving image")
            with open("temp_image.jpg", "wb") as f:
                f.write(response.content)
        else:
            print("Failed to download image.")

        postToSlack()
    else: print("Meme error: ", response)


def count():    

    global imgflipUser 
    global imgflipPass 
    global slackToken
    global eventID

    if path.exists('private.yaml'):
      yamlFile = 'private.yaml'
    else:
      print("Error: Cannot locate settings file")
      sys.exit(1)

    with open(yamlFile) as settingsFile:
      settings = yaml.load(settingsFile, Loader = yaml.FullLoader)
      #print (settings)

      token = settings['humanitix-api-key']
      imgflipUser = settings['imgflip-username']
      imgflipPass = settings['imgflip-password']
      slackToken = settings['slack-the-count-token']
      eventID = settings['humanitix-event-id']
      
    url = "https://api.humanitix.com/v1/events/" + eventID +  "/tickets?page=1"

    headers = {
        "x-api-key": token
        }

    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        #print("Response:", response.text)
        data = response.json()
        total = data.get("total")
        print("Total Tickets:", total)

        #get last count        
        with open("tickets-last-count.txt", "r") as file:
            total_last = int(file.read())
        print ("Last Count:   ", total_last)

        if total > total_last: 
            print("Creating new image")
            createImage(total)

            #print("Saving current count")
            with open("tickets-last-count.txt", "w") as file:
                file.write(str(total))
        else: print("No change in ticket count - exiting.")

    else:
        #print(f"Failed with status code: {response.status_code}")
        print(f"Failed with status text: {response.text}")


def main():
    count()

if __name__ == "__main__":
    main()

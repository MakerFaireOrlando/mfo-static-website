
#make sure you install the jotform-api-python from github not just with pip vanilla
#the vanilla pip install doesnt support python3
#pip install git+git://github.com/jotform/jotform-api-python.git

#sept 2024 - I had to do the following on windows
#pip install git+https://github.com/jotform/jotform-api-python.git


from jotform import *        #see notes above 
import pprint
import sys
import yaml                  #pip install pyyaml
from slugify import slugify  #pip install python-slugify for python3
import unicodedata
import os
import os.path
import urllib
from urllib import request
from urllib import parse
from urllib.parse import urlparse
import time
import getopt
import requests
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import textwrap

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import matplotlib.pyplot as plt

#from urlparse import urlparse    python2

#import requests
import datetime

import os.path
from os import path

#settings
formFTD = "MFO2025 - Field Trip Day"

# get item from jotform answers list
def getAnswer (sub, id):
  #idStr = str(id).encode("utf-8").decode("utf-8")
  answer = sub["answers"].get(str(id)).get('answer')
  #sanitize any quotes in the answer
  #but don't do it if variable is List or None
  if isinstance(answer, str):
    answer = answer.replace('"', '')

  return answer

def getAnswerByName (aDict, id):
  try:
    answer = aDict.get(id)
    #sanitize any quotes in the answer
    #but don't do it if variable is List or None
    if isinstance(answer, str):
      answer = answer.replace('"', '')
    return answer
  except :
    print ("Error: getAnswerByName - " + id)
    sys.exit(1)


def createImage(image_path, top_text, bottom_text, font_path='impact.ttf', font_size=120):
    # Load image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    image_width, image_height = img.size

    # Load font
    font = ImageFont.truetype(font_path, font_size)

    def draw_text(text, position):
        # Wrap text to fit image width
        char_width, char_height = font.getsize('A')
        max_chars_per_line = image_width // char_width
        text = textwrap.fill(text.upper(), width=max_chars_per_line)

        # Get text size
        text_size = draw.textsize(text, font=font)

        # Calculate position
        x = (image_width - text_size[0]) / 2
        y = position

        # Draw outline
        outline_range = 4
        for dx in range(-outline_range, outline_range + 1):
            for dy in range(-outline_range, outline_range + 1):
                draw.text((x + dx, y + dy), text, font=font, fill='black')

        # Draw main text
        draw.text((x, y), text, font=font, fill='white')

    # Draw top and bottom text
    draw_text(top_text, 0)
    draw_text(bottom_text, image_height - font_size * 1.5)

    # Save or show
    #img.show()
    img.save('ftd_temp_image.jpg')


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

   
    # Upload the image to Slack
    try:
        response = client.files_upload_v2(
            channel="C07NS90SBFE", #for private channels, you have to use the channel ID 
                                    #which you get from the url in the web version
                                    #also - be careful, some syntax shows this as channels=
                                    #lost over an hour on that one :(
            file="ftd_temp_image.jpg",
            title="Update"
            #,request_file_info = False
        )
        print("Image uploaded successfully:", response["file"]["permalink"])
    except SlackApiError as e:
        print("Error uploading file:", e.response["error"])
        print(e.response)
        if e.response["error"] == "missing_scope":
            print(e.response["needed"]) #this will tell us a missing permission scope 

def export(outputAll):

    global slackToken

    countSubmissions = 0
    countStudents = 0
    countAdults = 0
    tally = {}

    # Prepare data for chart
    labels = []
    sizes = []
    total_participants = sum(v["numStudents"] + v["numAdults"] for v in tally.values())
 
    if path.exists('private.yaml'):
      yamlFile = 'private.yaml'
    else:
      print("Error: Cannot locate settings file")
      sys.exit(1)

    with open(yamlFile) as settingsFile:
      settings = yaml.load(settingsFile, Loader = yaml.FullLoader)
      #print (settings)

      token = settings['jotform-api-key']
      print ('API Key:  ', token)
      slackToken = settings['slack-the-count-token']
     

    jotformAPIClient = JotformAPIClient(token)

    forms = jotformAPIClient.get_forms()

    for form in forms:

      if form["title"] == formFTD:

        print("-------------------------------------------")
        print (form["title"])
        #print form
        print(form["id"] + " " + form["title"])
        submissions = jotformAPIClient.get_form_submissions(form["id"], limit = 1000)
        for sub in submissions:
          ans ={}
          answers = sub["answers"]

          for id, info in answers.items():
            if "answer" not in info:
              continue

            if "name" in info:
              ans[info["name"]] = info["answer"]

          countSubmissions = countSubmissions+1

          role = getAnswerByName (ans, "participantRole")
          
          numStudents = int(getAnswerByName (ans, "numStudents"))
          numAdults = int(getAnswerByName (ans, "numAdults"))
          #print(role, " Students: ", numStudents, " Adults: ",  numAdults)
          countStudents = countStudents + numStudents
          countAdults = countAdults + numAdults
          
          if role not in tally:
            tally[role] = {"numStudents": 0, "numAdults": 0}

          tally[role]["numStudents"] += numStudents
          tally[role]["numAdults"] += numAdults

    #todo: count regular CFM vs Ruckus CFM separately and also give total
    print("---")
    print("Submissions Found: " + str(countSubmissions))
    print("Total Students: " + str(countStudents))
    print("Total Adults: " + str(countAdults))
    print("Total Attendees: " + str(countStudents + countAdults))
    print("---")
    
    # Print the result
    for role, counts in sorted(tally.items()):
      totalRole = counts['numStudents'] + counts['numAdults']
      percentRole = totalRole / (countStudents + countAdults) * 100
      print(f"{role}: {counts['numStudents']} students, {counts['numAdults']} adults, {totalRole} total {percentRole:.1f}%")

    # Example usage
    topText = f"{countStudents + countAdults} Riders"
    createImage('makey_bus.jpg', topText , 'ON THE BUS!')
    postToSlack()




def main():

    outputAll = False

    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "ho:"

    # Long options
    long_options = ["help", "option"]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                print ("usage: python3 update_exhibits.py [-o option]")
                print ("Options and arguments:")
                print ("-o rebuild :    Rebuild all exhibits")
                sys.exit()

            elif currentArgument in ("-o", "--option"):
                if currentValue == "rebuild":
                    outputAll = True
                    print("opttion: outputAll = ", outputAll)

        export(outputAll)

    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))


if __name__ == "__main__":
    main()


#make sure you install the jotform-api-python from github not just with pip vanilla
#the vanilla pip install doesnt support python3
#pip install git+git://github.com/jotform/jotform-api-python.git


from jotform import *
import pprint
import sys
import yaml
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
import csv
import requests

#from urlparse import urlparse    python2

#import requests
from PIL import Image, ExifTags, ImageOps       #pip install pillow (not pil)
import datetime

import os.path
from os import path

#settings
eventYear = 2023
formCFM = "Call For Makers MFO2023"
formRuckus = "CFM - Ruckus - MFO2023"


outputAll = False #this is now set with a command line param, don't change it here


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



def export():

    countSubmissions = 0
    countVisible = 0

    totalTickets = 0
    ticketList = [["Order Id", "Ticket Type", "Buyer First Name", "Buyer Last Name", "Buyer Email", "Buyer Mobile", "ZIP Code"]]
    ticketCountList = [["Exhibit Id", "Exhibit Name", "Exhibit URL", "First Name", "Last Name", "Email", "Tickets"]]

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

    jotformAPIClient = JotformAPIClient(token)

    forms = jotformAPIClient.get_forms()

    for form in forms:
      #print form["title"]


      if form["title"] == formCFM or form["title"] == formRuckus:

        #we need to know later what we are processing
        if form["title"] == formCFM:
          isRuckus = False
        elif form["title"] == formRuckus:
          isRuckus = True

        print("-------------------------------------------")
        print (form["title"])
        #print form
        print(form["id"] + " " + form["title"])
        submissions = jotformAPIClient.get_form_submissions(form["id"], limit = 1000)
        for sub in submissions:
          ans ={}
          answers = sub["answers"]

          for id, info in answers.items():
            #print(id + ": " + info["name"])
            #print("name: " +  info["name"])

            #for key in info:
            # print(key + ':', info[key])

            #looking only for the items with user responses
            if "answer" not in info:
              continue



            #print("answer: " +  info["answer"])

            #add to our simplified dictionary

            if "name" in info:
              ans[info["name"]] = info["answer"]

          #print (ans)
          countSubmissions = countSubmissions+1

          exhibitName = getAnswerByName (ans, "exhibitName")
          mfoID = getAnswerByName(ans,"exhibitId")

          if exhibitName is None:
            continue

          exhibitName = exhibitName.strip()
          mfoID = mfoID.strip()

          #slugify and remove apostrophes so they don't turn into dashes
          #slug = slugify(exhibitName, replacements = [["'", ""]])  python2
          slug=slugify(exhibitName.replace("'", "")) #python3

          exhibitURL = "https://www.makerfaireorlando.com/exhibits/" + slug + "/"

          viz = False
          vizAns = getAnswerByName(ans,"visibility")

          if vizAns:
            if 'Show on Website' in vizAns:
              viz = True

          if viz == True:
            countVisible = countVisible+1

            makerFirstName  = getAnswerByName(ans,"name")["first"]
            makerLastName   = getAnswerByName(ans,"name")["last"]
            makerPhone      = getAnswerByName(ans,"phoneNumber")['full']
            makerZIP        = getAnswerByName(ans,"address")["postal"]
            makerEmail      = getAnswerByName(ans,"email")
            makerTickets    = int(getAnswerByName(ans,"helperApproved")) + 1

            totalTickets = totalTickets + makerTickets

            print (mfoID, makerFirstName, makerLastName, makerPhone, makerZIP, makerEmail, makerTickets)

            ticketCountList.append([mfoID, exhibitName, exhibitURL, makerFirstName, makerLastName, makerEmail, makerTickets])

            for t in range (makerTickets):
                ticketList.append([mfoID, "Maker / Maker Helper", makerFirstName, makerLastName, makerEmail, makerPhone, makerZIP])



          #jotform currently does not let you change the field name of these image fields :(
          #it looks possible via API, but trying to keep it simple at the moment :)

    #print(ticketCountList)
    #print (ticketList)
    print("Submissions Found: " + str(countSubmissions))
    print("Submissions Visible: " + str(countVisible))
    print("Total Tickets: " + str(totalTickets))

    with open("maker-tickets.csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(ticketList)

    with open("maker-ticket-count.csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(ticketCountList)

def main():

    export()

if __name__ == "__main__":
    main()

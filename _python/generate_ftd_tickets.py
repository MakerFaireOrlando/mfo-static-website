
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
formFTD = "MFO2025 - Field Trip Day"


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
    countSmallGroups = 0

    totalTickets = 0
    ticketList = [["Order Id", "Ticket Type", "Buyer First Name", "Buyer Last Name", "Buyer Email", "Buyer Mobile"]]
    ticketCountList = [["Request Id", "First Name", "Last Name", "Phone" ,"Email", "Tickets"]]

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


      if form["title"] == formFTD:
        
        print("-------------------------------------------")
        print (form["title"])
        #print form
        print(form["id"] + " " + form["title"])
        submissions = jotformAPIClient.get_form_submissions(form["id"], limit = 1000)
        for index, sub in enumerate(submissions):
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
          
          firstName  = getAnswerByName(ans,"name")["first"]
          lastName   = getAnswerByName(ans,"name")["last"]
          phone      = getAnswerByName(ans,"phoneNumber")['full']
          email      = getAnswerByName(ans,"email")
          numStudents  = int(getAnswerByName(ans,"numStudents"))
          numAdults    = int(getAnswerByName(ans,"numAdults"))
          numTickets   = numStudents + numAdults

          if numTickets > 9: 
            continue

          countSmallGroups = countSmallGroups + 1
          totalTickets = totalTickets + numTickets

          id = "MFO-FTD-" + str(index+1) #dont start at zero

          print (id, firstName, lastName, phone, email, numStudents, numAdults, numTickets)

          ticketCountList.append([id, firstName, lastName, phone, email, numTickets])

          for t in range (numTickets):
              ticketList.append([id, "Field Trip Day Attendee", firstName, lastName, email, phone])


    #print(ticketCountList)
    #print (ticketList)
    print("Submissions Found: " + str(countSubmissions))
    print("Small Groups Found: " + str(countSmallGroups))
    print("Total Small Group Tickets: " + str(totalTickets))

    with open("ftd-tickets.csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(ticketList)

    with open("ftd-ticket-count.csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(ticketCountList)

def main():

    export()

if __name__ == "__main__":
    main()

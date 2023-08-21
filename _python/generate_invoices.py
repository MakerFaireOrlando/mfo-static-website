
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


def export(outputAll):

    countSubmissions = 0
    countVisible = 0
    fniCount = 0
    spaceplanList = []

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

          viz = False
          vizAns = getAnswerByName(ans,"visibility")

          if vizAns:
            if 'Show on Website' in vizAns:
              viz = True

          if viz == True:
            countVisible = countVisible+1

          makerName       = getAnswerByName(ans,"makerName")
          makerDesc       = getAnswerByName(ans,"makerDesc")
          feeStatus       = getAnswerByName(ans,"feeStatus")
          email           = getAnswerByName(ans,"email")
          name           = getAnswerByName(ans,"name")
          print(mfoID, exhibitName, email, name['first'], name['last'])      

          if (feeStatus):
              print(mfoID + " " + exhibitName + ": " + str(viz) + ", " + feeStatus)
              if 'Fee Not Invoiced' in feeStatus:
                print ("Generate Invoice!")
                fniCount = fniCount+1




          #jotform currently does not let you change the field name of these image fields :(
          #it looks possible via API, but trying to keep it simple at the moment :)


    #todo: count regular CFM vs Ruckus CFM separately and also give total
    print("Submissions Found: " + str(countSubmissions))
    print("Submissions Visible: " + str(countVisible))
    print("Fees Not Invoiced: " + str(fniCount))

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

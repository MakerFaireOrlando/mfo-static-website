
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
import csv
import requests
from collections import Counter

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

def export(outputAll):

    countSubmissions = 0
    countStudents = 0
    countAdults = 0
    tally = {}
 
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
    print("Submissions Found: " + str(countSubmissions))
    print("Total Students: " + str(countStudents))
    print("Total Adults: " + str(countAdults))
    print("Total Attendees: " + str(countStudents + countAdults))
    
    # Print the result
    for role, counts in tally.items():
      print(f"{role}: {counts['numStudents']} students, {counts['numAdults']} adults, {counts['numStudents'] + counts['numAdults']} total")

    

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

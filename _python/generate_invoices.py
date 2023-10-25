
#todo: only pull approved exhibits

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
from datetime import datetime as dt

#from urlparse import urlparse    python2

#import requests
import datetime

import os.path
from os import path

#PAYPAL_URL = 'https://api-m.sandbox.paypal.com'
PAYPAL_URL = 'https://api-m.paypal.com'

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



#settings
eventYear = 2023
formCFM = "Call For Makers MFO2023"
formRuckus = "CFM - Ruckus - MFO2023"

outputAll = False #this is now set with a command line param, don't change it here



def doPayPalAuth(pp_client_id, pp_client_secret):

    #print ('PayPay Client ID:\t ', pp_client_id)
    #print ('PayPal Client Secret\t  ', pp_client_secret)

    oauth_url = '%s/v1/oauth2/token' % PAYPAL_URL

    oauth_response = requests.post(oauth_url,
                                   headers= {'Accept': 'application/json',
                                             'Accept-Language': 'en_US'},
                                   auth=(pp_client_id, pp_client_secret),
                                   data={'grant_type': 'client_credentials'})

    # Get OAuth JSON in response body
    oauth_body_json = oauth_response.json()
    # Get access token
    #print("PayPal Access Token:\t ", oauth_body_json['access_token'])
    return oauth_body_json['access_token']

def findPayPalInvoice(token, exhibitID):

    invoiceData = { "invoice_number": "MFO-" + exhibitID }

    print (color.DARKCYAN + "Search:", "MFO-" + exhibitID+"->", end="" )
    invoice_url = '%s/v2/invoicing/search-invoices' % PAYPAL_URL

    invoice_response = requests.post(invoice_url,
                                   headers= {'Accept': 'application/json',
                                             'Accept-Language': 'en_US',
                                             'Authorization': f'Bearer {token}'},
                                   json=invoiceData)



    invoice_body_json = invoice_response.json()

    if ("items" in invoice_body_json):
        print ("Invoice status is: ", end="")
        print (invoice_body_json['items'][0]['status'], end="->")
        return invoice_body_json['items'][0]['status']
    else:
        print ("Invoice does not exist->", end="")
        return "not-found"


def createPayPalInvoice(token, exhibitID, makerEmail, makerFirstName, makerLastName, exhibitName, type, fee):
    invoiceData = {
        "detail": {
            "invoice_number": "",
            "invoice_date": "",
            "payment_term": {
                "term_type": "NET_10",
                "due_date": ""
            },
            "currency_code": "USD",
            "note": "",
            "memo": "Created via automated script."
        },
        "invoicer": {
            "business_name": "The Maker Effect Foundation",
            "email_address": "treasurer@themakereffect.org",
            "logo_url": "https://pics.paypal.com/00/s/NTU1WDE3MTFYUE5H/p/Y2Y0ZWIxODMtMTFmZS00YTQxLTlkMzktNzUwZmIwYjIzN2Vh/image_109.PNG"
        },
        "primary_recipients": [
            {
                "billing_info": {
                    "name": {
                        "given_name": "",
                        "surname": ""
                    },
                    "email_address": ""
                }
            }
        ],
        "items": [
            {
                "name": "",
                "description": "",
                "quantity": "1",
                "unit_amount": {
                    "currency_code": "USD",
                    "value": "100.00"
                },
                "unit_of_measure": "AMOUNT"
            }
        ]
    }


    invoiceData['detail']['invoice_date'] = dt.today().strftime('%Y-%m-%d')
    dueDate = dt.today() + datetime.timedelta(days=10)
    invoiceData['detail']['payment_term']['due_date'] = dueDate.strftime('%Y-%m-%d')


    invoiceData['primary_recipients'][0]['billing_info']['name']['given_name'] = makerFirstName
    invoiceData['primary_recipients'][0]['billing_info']['name']['surname'] = makerLastName
    invoiceData['primary_recipients'][0]['billing_info']['email_address'] = makerEmail

    if (type == 'seller'):
        invoiceData['detail']['invoice_number'] = "MFO-" + exhibitID
        invoiceData['items'][0]['description'] = "Exhibit: " + exhibitName
        invoiceData['items'][0]['name'] = "Maker Faire Orlando - Seller Fee"
        invoiceData['items'][0]['unit_amount']['value']= fee
        invoiceData['detail']['note'] = "Thank you for exhibiting at Maker Faire Orlando! Please pay your seller fee promptly to avoid losing your exhibit placement."

    elif (type == 'ruckus'):
        invoiceData['detail']['invoice_number'] = "MFO-" + exhibitID
        invoiceData['items'][0]['description'] = "Robot: " + exhibitName
        invoiceData['items'][0]['name'] = "Robot Ruckus - Entry Fee"
        invoiceData['items'][0]['unit_amount']['value']= fee
        invoiceData['detail']['note'] = "Thank you for competing at Robot Ruckus! Please pay your entry fee promptly to avoid losing your spot in the competition."

    else:
        print ("ERROR, UNKNOWN TYPE OF INVOICE!!!!!!")
        sys.exit(0)


    #print (invoiceData)

    #use this when we don't want it to work
    #token = "fail-auth-for-testing"

    invoice_url = '%s/v2/invoicing/invoices' % PAYPAL_URL

    invoice_response = requests.post(invoice_url,
                                   headers= {'Accept': 'application/json',
                                             'Accept-Language': 'en_US',
                                             'Authorization': f'Bearer {token}'},
                                   json=invoiceData)


    invoice_body_json = invoice_response.json()

    #print (invoice_response.status_code, invoice_body_json)
    return invoice_response.status_code


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
    countFeeSent = 0
    countFeeDraft = 0
    countFeePaid = 0
    countFeeWaived = 0
    countFeeWaived = 0
    countInvoiceGenerated = 0
    countFeeNotReq = 0
    countSelling = 0
    countRobots = 0

    if path.exists('private.yaml'):
      yamlFile = 'private.yaml'
    else:
      print("Error: Cannot locate settings file")
      sys.exit(1)

    with open(yamlFile) as settingsFile:
      settings = yaml.load(settingsFile, Loader = yaml.FullLoader)
      #print (settings)

      jf_token = settings['jotform-api-key']


      #print ('JotForm API Key:  ', jf_token)

    jotformAPI = JotformAPIClient(jf_token)
    forms = jotformAPI.get_forms()

    #get PayPal token
    pp_access_token = doPayPalAuth(settings['paypal-client-id'], settings['paypal-client-secret'])

    #get data from JotForm

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
        #print(form["id"] + " " + form["title"])


        #if (isRuckus==False):
        #    questions = jotformAPI.get_form_questions(form["id"])
    #        print(questions)
    #        sys.exit(0)

        submissions = jotformAPI.get_form_submissions(form["id"], limit = 1000)
        for sub in submissions:
          ans ={}
          answers = sub["answers"]
          #print(sub)
          submission_id = sub['id']
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

          #hack for an invoice that WOULD NOT generate would always report cancelled
          #if (mfoID == "22R-16"): mfoID = "22R-16-F"

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

          #print(mfoID, exhibitName, email, name['first'], name['last'])
          if (feeStatus):
              if ('Fee Not Invoiced' in feeStatus or 'Fee Due' in feeStatus or 'Fee Paid' in feeStatus or 'Fee Waived' in feeStatus):
                  if (not isRuckus): countSelling = countSelling + 1
                  if (isRuckus): countRobots = countRobots + 1


          if (feeStatus and viz):

            if ('Fee Not Invoiced' in feeStatus or 'Fee Due' in feeStatus):
                print(color.DARKCYAN + feeStatus + "\t\t" +  mfoID + "\t" + exhibitName + "->" + color.END, end = "")
                #print ("Generating Invoice...", end="" )
                if (isRuckus):
                    iType = "ruckus"
                    fee = getAnswerByName(ans,"registrationFee")
                else:
                    iType = "seller"
                    fee = "100.00"


                findResp = findPayPalInvoice(pp_access_token, mfoID)
                if ("not-found" in findResp):
                    invResp = createPayPalInvoice(pp_access_token, mfoID, email, name['first'], name['last'], exhibitName, iType, fee)
                    if (invResp == 201):
                      print ("Invoice Generated" + color.END)
                      countInvoiceGenerated = countInvoiceGenerated + 1
                    else: print ("ERROR GENERATING INVOICE!" + color.END)
                elif ("DRAFT" in findResp):
                    print (color.BOLD + "LOGIN TO PAYPAL AND SEND THE INVOICE!!" + color.END)
                    countFeeDraft = countFeeDraft + 1
                elif ("SENT" in findResp):
                    if (not "Fee Due" in feeStatus):
                        print ("UPDATE JOTFORM TO 'Fee Due'")
                        if (isRuckus): jotformAPI.edit_submission(submission_id, {"114": "Fee Due"})
                        else: jotformAPI.edit_submission(submission_id, {"117": "Fee Due"})
                    else: print ("Done" + color.END)
                    countFeeSent = countFeeSent + 1
                elif ("PAID" in findResp):
                    print ("UPDATE JOTFORM TO 'Fee Paid'")
                    if (isRuckus): jotformAPI.edit_submission(submission_id, {"114": "Fee Paid"})
                    else: jotformAPI.edit_submission(submission_id, {"117": "Fee Paid"})
                    countFeePaid = countFeePaid + 1
                    if (not isRuckus): countSelling = countSelling +1
                else:
                    print ("ERROR: UNKNOWN STATUS!")

                #sys.exit(0)

                fniCount = fniCount+1

                #limit number of invoices created when testing
                #if (fniCount >=5): sys.exit(0)

            else:
                 if (not "Fee Not Required" in feeStatus and not "Fee Waived" in feeStatus ):
                    if ("Fee Paid" in feeStatus):
                        countFeePaid = countFeePaid + 1
                        print(color.GREEN + feeStatus  + "\t" + mfoID + "\t" + exhibitName, color.END)
                    else: print(feeStatus + " \t", mfoID + "\t" + exhibitName)

                 if ("Fee Waived" in feeStatus):
                    countFeeWaived = countFeeWaived + 1
                 elif ("Fee Not Required" in feeStatus):
                    countFeeNotReq = countFeeNotReq + 1

          else:
              if (viz): print(color.BOLD + color.RED + "NO FEESTATUS\t" +  mfoID + "\t" +  exhibitName, color.END)
              #print(color.BOLD + 'Hello, World!' + color.END)



          #jotform currently does not let you change the field name of these image fields :(
          #it looks possible via API, but trying to keep it simple at the moment :)


    #todo: count regular CFM vs Ruckus CFM separately and also give total
    print("\r\r---------------------------------------------------------------------------")
    print("Submissions Found: " + str(countSubmissions))
    print("Submissions Visible (Approved): " + str(countVisible))

    totalInvoiced = countFeeDraft + countFeeSent + countFeePaid
    print("Total Invoiced: " + str(totalInvoiced))
    print("Combot Robots: " + str(countRobots))
    print("Selling: " + str(countSelling))
    print("% Vendor {:.1f}%".format((countSelling/countVisible)*100))
    print("---------------------------------------------------------------------------")
    print("Fees Not Required: " + str(countFeeNotReq))
#    print("Fees Waived: " + str(countFeeWaived))
    print("Fees Not Invoiced: " + str(fniCount))
    print("Invoices Generated: " + str(countInvoiceGenerated))
    print("Fees Draft: " + str(countFeeDraft))
    print("Fees Sent: " + str(countFeeSent))
    print("Fees Paid: " + str(countFeePaid))
    print("---------------------------------------------------------------------------")
    #print("Paid %:" + str(countFeePaid / countFeeSent) * 100)
    print(color.BOLD + "Paid {:.1f}%".format((countFeePaid / (countFeeSent + countFeePaid))*100) + color.END)
    print("")
    print("")


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


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
from PIL import Image, ExifTags, ImageOps       #pip install pillow (not pil)
import datetime

import os.path
from os import path

#settings
eventYear = 2025
formCFM = "Call For Makers MFO2025"
formRuckus = "CFM - Ruckus - MFO2025"


outputAll = False #this is now set with a command line param, don't change it here



#todo: write the exhibit URL back to jotform for easy linking :)
#todo: remove withdrawn / cancelled exhibits...


#image resizing: https://stackoverflow.com/questions/8631076/what-is-the-fastest-way-to-generate-image-thumbnails-in-python

#NOTE: Image pulls will fail unless you go to jotform settings for the account and
#       remove the requirement to be logged in to see uploaded items


def exportCategories(categories: Counter):
  exported = []
  optionStringFull =""

  for name, count in sorted(categories.items(), key=lambda x: x[0].lower()):
      
      slug = slugify(name)
      exported.append({
          "name": name,
          "slug": slug,
          "count": count
      })
      print (name, slug, count)
      option_str = f'<option value=".{slug}">{name} ({count})</option>'
      print (option_str)
      optionStringFull+=option_str

      #title: "Learn to Solder"
      #slug: mfo-learn-to-solder
      #permalink: /exhibits/mfo-learn-to-solder/
      fn = "../_categories/" + slug + ".md"
      with open(fn, "w", encoding="utf-8") as catfile:
        catfile.write("---\n")
        catfile.write("title: " + '"' + name + '"' + "\n")
        catfile.write("slug: " + slug + "\n")
        catfile.write("permalink: /exhibits/categories/" + slug + "/\n")
        catfile.write("description: Check out all the " + name + " exhibits at Maker Faire Orlando!\n") #for SEO
        catfile.write("image: /assets/images/site-branding/mfo_two_line_border.png\n") #for SEO
        catfile.write("isotope: true\n") #get that JS included
        catfile.write("\n\n\n---\n")
  
  #print(optionStringFull)
  with open("../_includes/category-options.html", "w", encoding="utf-8") as file:
    file.write(optionStringFull)

  return exported


#get youtube embed from watch url using oembed API
def getYouTubeEmbed (url):
  reqURL = "https://www.youtube.com/oembed?url=" + url + "&format=json&maxwidth=1024&maxheight=1024"
  response = requests.get(reqURL)
  print ("Printing YouTube Response: ", response.text)
  if (response.text=="Not Found"):
    return None
  rjson = response.json()
  return (rjson["html"].replace("'", ""))

#output csv file from list
def writeCSVFile (fn, data):
  with open(fn, mode='w', encoding="utf-8") as csvFile:
    csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    for row in data:
      csvWriter.writerow(row)

  csvFile.close()


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

# save image locally if not exists
# return local url
def processImage(eid, eslug, type, url):

  a = parse.urlparse(url)
  aFn, aFnExt = os.path.splitext(url)
  #print aFnExt
  last = slugify(aFn.rsplit('/', 1)[-1])
  #print(last)

  base = "../assets/images/exhibit-images/" + eid + "-" + type + "-" + eslug + "-" + last
  fullFn      = base + "-full"    + aFnExt
  smallFn     = base + "-small"   + aFnExt
  mediumFn    = base + "-medium"  + aFnExt
  largeFn     = base + "-large"   + aFnExt

  filenames = (smallFn, mediumFn, largeFn, fullFn)

  if not path.exists(fullFn):
    url = url.replace(" ", "%20")
    print ("Downloading: " + url)

    #from https://www.py4u.net/discuss/12680
    url = urllib.parse.urlsplit(url)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    print(url)

    #print (fullFn)
    #resource = urllib.request.urlopen(url)
    import requests
    r = requests.get(url)
    #print (r)

    #print (resource)
    output = open(fullFn,"wb")
    output.write(r.content)
    output.close()

  if not path.exists(smallFn):
    # creating a object
    image = Image.open(fullFn)
    image = ImageOps.exif_transpose(image)
    image.thumbnail((150,150))
    image.save(smallFn)

  if not path.exists(mediumFn):
    # creating a object
    image = Image.open(fullFn)
    image = ImageOps.exif_transpose(image)
    image.thumbnail((300,300))
    image.save(mediumFn)

  if not path.exists(largeFn):
    # creating a object
    image = Image.open(fullFn)
    image = ImageOps.exif_transpose(image)
    image.thumbnail((1024,1024))
    #23-135 yielded error - https://stackoverflow.com/questions/21669657/getting-cannot-write-mode-p-as-jpeg-while-operating-on-jpg-image
    #should I do this for every size??
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(largeFn)


  return filenames

def socialURLClean(url,name):
  social = urlparse(url)
  social = social._replace(scheme = "https")
  social = social._replace(netloc = "www." + name + ".com")

  #YouTube URLs are case sensitive, so removing the .lower()
  #socialpath = social.path.lower()
  socialpath = social.path

  socialpath = socialpath.replace("www." + name + ".com","")
  socialpath = socialpath.replace(name + ".com","")
  #socialpath = socialpath.replace("/","")
  socialpath = socialpath.replace("www.","")
  socialapath = socialpath.replace("www","")
  social = social._replace(path = socialpath)
  return social.geturl()

def urlClean(url):
  site = urlparse(url)
  if site.scheme == "":
    site = site._replace(scheme = "https")
  sitepath = site.path.lower()
  site = site._replace(path = sitepath)
  return site.geturl().replace("///", "//")

def export(outputAll):

    countSubmissions = 0
    countVisible = 0
    countExhibitsRemoved = 0
    countExport = 0
    countFTD=0

    uniqueCategories = Counter()

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

          #slugify and remove apostrophes so they don't turn into dashes
          #slug = slugify(exhibitName, replacements = [["'", ""]])  python2
          slug=slugify(exhibitName.replace("'", "")) #python3

          # fName is the full name of the exhibit markdown file
          # Variable established this early so that if exhibit is no longer
          #     visible we can confirm the exhibit file is removed
          fName = "../_exhibits/" + str(eventYear) + "-" +slug + ".md"

          viz = False
          vizAns = getAnswerByName(ans,"visibility")

          if vizAns:
            if 'Show on Website' in vizAns:
              viz = True

          if viz == True:
            countVisible = countVisible+1

          else:
            if path.exists(fName):
                print("***" + mfoID + " " + exhibitName + " is no longer visible")
                os.remove(fName)
                # print("ALERT: need to remove exhibit file ", fName)
                countExhibitsRemoved = countExhibitsRemoved+1
            continue

          print(mfoID + " " + exhibitName + ": " + str(viz))

          descShort       = getAnswerByName(ans,"exhibitShort")
          descLong        = getAnswerByName(ans,"exhibitLong")

          if isRuckus:
            spaceNumber = ""
            exhibitZone = "Robot Ruckus (Spirit Building)"
          else:
            spaceNumber = getAnswerByName(ans,"spaceNumber")
            exhibitZone = getAnswerByName(ans,"exhibitZone")
            #note, there could be multiple exhibitZones

          categories      = getAnswerByName(ans,"exhibitCategories")
          

          #added july 2025 for Field Trip Day
          exhibitAvail = getAnswerByName(ans, "exhibitAvailability51")
          if ("Education Day" in exhibitAvail) or ("Field Trip Day" in exhibitAvail):  
            categories.append("Field Trip Day")
            if viz == True:
              countFTD = countFTD + 1
              
          uniqueCategories.update(categories)
            
          exhibitImage    = processImage(mfoID,slug,"exhibit",getAnswerByName(ans,"exhibitImage")[0])

          exhibitAddlImages = getAnswerByName(ans,"exhibitImage44")

          exhibitVideo    = getAnswerByName(ans,"exhibitYouTube")

          exhibitWebsite  = getAnswerByName(ans,"exhibitWebsite")
          makerName       = getAnswerByName(ans,"makerName")
          makerDesc       = getAnswerByName(ans,"makerDesc")

          #jotform currently does not let you change the field name of these image fields :(
          #it looks possible via API, but trying to keep it simple at the moment :)

          makerImage      = processImage(mfoID,slug,"maker",getAnswerByName(ans,"maker18")[0])
          makerEmail      = getAnswerByName(ans,"makerEmail")
          makerWebsite    = getAnswerByName(ans,"makerWebsite")
          makerTwitter    = getAnswerByName(ans,"makerTwitter")
          makerInstagram  = getAnswerByName(ans,"makerInstagram")
          makerFacebook   = getAnswerByName(ans,"makerFacebook")
          makerYouTube    = getAnswerByName(ans,"makerYouTube")
          makerTikTok     = getAnswerByName(ans,"makerTikTok")

          #split the spaceNumber field
          #for each spaceNumber
          #append to the list the data needed

          if spaceNumber is not None and spaceNumber != "":
            snList = spaceNumber.split(",")
            for sn in snList:
              #todo: get fee details to append in the sEID field
              sn = sn.strip().upper()

              #SUPRESS DUPLICATE SPACE NUMBERS for shared exhibits
              #If there is not an existing list item with same sn, then keep going
              #if there is, I'd like to kill it - OR replace it with a modified entry that captured both
              #What is the pythonic way to search the list of lists?

              dup = False

              for spList in spaceplanList:      #is this space number already in the spaceplanList
                spListN = spList[:1]


                if (sn in spListN):
                  spList[1] = '> > ' + spList[1] #this is the text that goes in the field
                  spList[2] = '> > ' + spList[2] #this is the text that goes in the field
                  spList[3] = '> > ' + spList[3] #this is the text that goes in the field
                  print("DUPLICATE", sn, spList)
                  dup = True

              if (exhibitName != makerName):
                sEID = sn + " : " + mfoID + "\\" + "\\" + exhibitName[0:20] + "\\" + "\\" + makerName[0:20]
              else:
                sEID = sn + " : " + mfoID + "\\" + "\\" + exhibitName[0:40]
              sEX = sn + "\\" + "\\" + exhibitName
              sEM = sn + "\\" + "\\" + exhibitName + "\\" + "\\" + makerName
              sE = exhibitName
              sList = [sn, sEID, sEX, sEM, sE]
              if (not dup):
                  spaceplanList.append(sList)
              else:
                  print("Skipping append since dup")



          # create Exhibit markdown file

          #check to see if last export date > last change date, and then we can skip
          #this will reduce the number of github updates
          export = True

          if path.exists(fName):
            with open(fName, encoding="utf-8") as yFile:
              yData = yaml.load_all(yFile, Loader = yaml.FullLoader)
              #print (yData)
              #parse(yData)
              for data in yData:
                if "last-exported" not in data:
                  export = True

                else:
                  lastExport = data.get('last-exported')

                  lastMod = sub["updated_at"]
                  #print ('last-exported: ', lastExport)
                  #print ('last-modified: ', lastMod)

                  dtExport = time.strptime(lastExport, '%Y-%m-%d %H:%M:%S')
                  dtMod    = time.strptime(lastMod, '%Y-%m-%d %H:%M:%S')

                  export = dtMod > dtExport

                  #print ('last-exported: ', dtExport)
                  #print ('last-modified: ', dtMod)

                  #print (export)

                  break
                  #only read from the first document

          if export or outputAll:

            countExport = countExport+1
            print("Exporting: " + fName)

            #get YouTube embed but only if we are updating the file!
            if exhibitVideo is not None:
              exhibitVideoEmbed = getYouTubeEmbed(exhibitVideo)

            outfile = open(fName, "w")
            outfile.write("---\n")
            outfile.write("# note: title, description, image are used for SEO\n")
            outfile.write("\n")

            #p2 outfile.write("title: " + '"' + exhibitName + '"' + "\n")
            outfile.write("title: " + '"' + exhibitName + '"' + "\n")
            outfile.write("slug: " + slug + "\n")
            outfile.write("permalink: /exhibits/" + slug + "/\n")
            outfile.write("exhibit-id: " + mfoID + "\n")

            if (isRuckus):
                outfile.write("combat-robot: true\n")

            if exhibitZone is not None:
              outfile.write("exhibit-zone: " + '"' + exhibitZone + '"' + "\n")

            if spaceNumber is not None:
              if len(spaceNumber) > 0:
                outfile.write("space-number: " + '"' + spaceNumber + '"' + "\n")
              else: #its not none, but still empty
                outfile.write("space-number: Unassigned\n")
            else: #it is none
              outfile.write("space-number: Unassigned\n")




            outfile.write("description: " + '"' + descShort + '"' + "\n")
            outfile.write("description-long: " + '"' + descLong + '"' + "\n")

            outfile.write("image: "   + exhibitImage[2][2:] + "\n")


            outfile.write("image-primary: \n")
            outfile.write("  small: "   + exhibitImage[0][2:] + "\n")
            outfile.write("  medium: "  + exhibitImage[1][2:] + "\n")
            outfile.write("  large: "   + exhibitImage[2][2:] + "\n")
            outfile.write("  full: "    + exhibitImage[3][2:] + "\n")

            if len(exhibitAddlImages) > 0:
              outfile.write("additional-images: \n")

            i=1
            for addlImage in exhibitAddlImages:

              image = processImage(mfoID,slug,"exhibit-addl" + str(i),addlImage)

              outfile.write("  - " + str(i) + ":\n")
              outfile.write("    small: "   + image[0][2:] + "\n")
              outfile.write("    medium: "  + image[1][2:] + "\n")
              outfile.write("    large: "   + image[2][2:] + "\n")
              outfile.write("    full: "    + image[3][2:] + "\n")
              i = i+1

            if exhibitWebsite is not None:
              outfile.write("website: " + '"' + urlClean(exhibitWebsite) + '"' + "\n")

            if exhibitVideo is not None:
              outfile.write("video: " + '"' + exhibitVideo + '"' + "\n")

              if exhibitVideoEmbed is not None:
                outfile.write("video-embed: " + "'" + exhibitVideoEmbed + "'" + "\n")


            #maker info
            outfile.write("maker: \n")
            outfile.write ("  name: " + '"' + makerName + '"' + "\n")
            outfile.write ("  description: " + '"' + makerDesc + '"' + "\n")
            outfile.write ("  image-primary: " + makerImage[1][2:] + "\n")

            #Let's stop listing email on the site, too easy to scrape...
            #if makerEmail is not None: outfile.write("email: " + makerEmail + "\n")
            if makerWebsite is not None:
              outfile.write("  website: " + urlClean(makerWebsite) + "\n")
            if makerTwitter is not None:
              outfile.write("  twitter: " + socialURLClean(makerTwitter, "twitter") + "\n")
            if makerInstagram is not None:
              #insta = urlparse(makerInstagram)
              #insta = insta._replace(scheme = "https")
              #insta = insta._replace(netloc = "www.instagram.com")
              #instapath = insta.path.lower()
              #instapath = instapath.replace("www.instagram.com","")
              #instapath = instapath.replace("instagram.com","")
              #instapath = instapath.replace("/","")
              #instapath = instapath.replace("www.","")
              #instapath = instapath.replace("www","")
              #insta = insta._replace(path = instapath)
              #outfile.write("  instagram: " + insta.geturl() + "\n")
              outfile.write("  instagram: " + socialURLClean(makerInstagram, "instagram") + "\n")

            if makerFacebook is not None:
              outfile.write("  facebook: " + socialURLClean(makerFacebook, "facebook") + "\n")

            if makerYouTube is not None:
              outfile.write("  youtube: " + socialURLClean(makerYouTube, "youtube") + "\n")

            if makerTikTok is not None:
              outfile.write("  tiktok: " + socialURLClean(makerTikTok, "tiktok") + "\n")


            #categories
            outfile.write("categories: \n")

            if isRuckus:
              category = "Combat Robots"
              outfile.write ("  - slug: " + slugify(category) + "\n")
              outfile.write ("    name: " + category + "\n")

            else:
              for category in categories:
                outfile.write ("  - slug: " + slugify(category) + "\n")
                outfile.write ("    name: " + category + "\n")

            #metadata
            outfile.write ("created-jotform: " + '"' + sub["created_at"] + '"' + "\n")
            outfile.write ("last-modified-jotform: " + '"' + sub["updated_at"] + '"' + "\n")

            now = datetime.datetime.now()
            outfile.write ("last-exported: " + '"' + now.strftime("%Y-%m-%d %H:%M:%S") + '"' + "\n")

            #don't include in sitemap
            outfile.write ("sitemap: false\n")

            outfile.write("\n---\n")
            outfile.close()

        

    if countExhibitsRemoved or countExport:
        print ("Exporting CSV files for Illustrator")
        #output our illustrator space plan file

        #order the list

        spaceplanList = sorted(spaceplanList, key=lambda x:x[0])
        #print (spaceplanList)

        #init the rows
        csvrowC = [["View"],["SpaceExhibitID"],["SpaceExhbit"],["SpaceExhibitMaker"],["Exhibit"]]
        csvrowS = [["View"],["SpaceExhibitID"],["SpaceExhbit"],["SpaceExhibitMaker"],["Exhibit"]]
        csvrowO = [["View"],["SpaceExhibitID"],["SpaceExhbit"],["SpaceExhibitMaker"],["Exhibit"]]

        #add blank spaces
        cRows = ['A','B','C','D','E','F','G','H','I','J']
        sRows = ['A','B','C','D','E','F','G','H','I','J','K','L']
        oRows = ['A','B','C','D','E','F','G']
        cNumCols = 6
        sNumCols = 36
        oNumCols = 29

        for curRow in cRows:
          for curCol in range(1,cNumCols + 1):
            curSpace = "C" + curRow + str(curCol)

            if any(e[0] == curSpace for e in spaceplanList) is False:
              csvrowC[0].append(curSpace)
              csvrowC[1].append("")
              csvrowC[2].append("")
              csvrowC[3].append("")
              csvrowC[4].append("")

        for curRow in sRows:
          for curCol in range(1,sNumCols + 1):
            curSpace = "S" + curRow + str(curCol)

            if any(e[0] == curSpace for e in spaceplanList) is False:
              csvrowS[0].append(curSpace)
              csvrowS[1].append("")
              csvrowS[2].append("")
              csvrowS[3].append("")
              csvrowS[4].append("")

        for curRow in oRows:
          for curCol in range(1,oNumCols + 1):
            curSpace = "O" + curRow + str(curCol)

            if any(e[0] == curSpace for e in spaceplanList) is False:
              csvrowO[0].append(curSpace)
              csvrowO[1].append("")
              csvrowO[2].append("")
              csvrowO[3].append("")
              csvrowO[4].append("")

        unow = datetime.datetime.now()
        updated = unow.strftime("%Y-%m-%d-%-H:%M:%S")
        updatedList = ["updated", updated, updated, updated, updated]


        #output by iterating the spaces
        for spc in spaceplanList:
          for row in range (0,5):
            #split by building
            if spc[0][0] == "C":
              csvrowC[row].append(spc[row])
            elif spc[0][0] == "S":
              csvrowS[row].append(spc[row])
            elif spc[0][0] == "O":
              csvrowO[row].append(spc[row])

        #add update time to end
        for urow in range (0,5):
          csvrowC[urow].append(updatedList[urow])
          csvrowS[urow].append(updatedList[urow])
          csvrowO[urow].append(updatedList[urow])

        writeCSVFile("curiosity.csv", csvrowC);
        writeCSVFile("spirit.csv", csvrowS);
        writeCSVFile("opportunity.csv", csvrowO);
    #end if changes then write export files

    #create include snippet with categories for the makers page
    exportCategories(uniqueCategories)

    #todo: count regular CFM vs Ruckus CFM separately and also give total
    print("Submissions Found: " + str(countSubmissions))
    print("Submissions Visible:", countVisible, f"{countFTD / countVisible * 100:.1f}%")
    print("Field Trip Day (Visible): " + str(countFTD))
    print("Exhibits Removed: " + str(countExhibitsRemoved))
    print("Exported: " + str(countExport))
    
    

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

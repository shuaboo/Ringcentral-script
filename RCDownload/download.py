from ringcentral import SDK
from ringcentral.http.api_exception import ApiException
import json
import yaml
import sys
import os
import time
from dateutil import parser
from datetime import datetime

#opens .yml file to set variables
conf = yaml.safe_load(open('./config.yml'))

RINGCENTRAL_CLIENTID = conf['user']['clientid']
RINGCENTRAL_CLIENTSECRET = conf['user']['clientsecret']
RINGCENTRAL_SERVER = 'https://platform.devtest.ringcentral.com'

RINGCENTRAL_USERNAME = conf['user']['username']
RINGCENTRAL_PASSWORD = conf['user']['password']
RINGCENTRAL_EXTENSION = '101'
MONTHSTART = conf['system']['monthstart']
#time in between API calls to not cause issues
TIMEPERAPICALL = 1200
#path to download to, change as needed
DOWNLOADPATH = conf['system']['downloadpath']

#login credentials
sdk = SDK( RINGCENTRAL_CLIENTID, RINGCENTRAL_CLIENTSECRET, RINGCENTRAL_SERVER )
platform = sdk.platform()
platform.login( RINGCENTRAL_USERNAME, RINGCENTRAL_EXTENSION, RINGCENTRAL_PASSWORD )

#gets the json object with voicemails
def getMessageStore():
    response = platform.get('/restapi/v1.0/account/~/extension/~/message-store',
        {
            'messageType': ['VoiceMail'],
            'dateFrom': MONTHSTART
        })

    return response.text()


#downloads voicemail
def downloadVoiceMails():
    messageStore = getMessageStore()
    #check if directory exists
    if not os.path.exists(DOWNLOADPATH):
        os.mkdir(DOWNLOADPATH)
    messageJSON = json.loads(messageStore)
    messageIDs = []
    timeStamps = []
    #access records to download all voicemails
    for record in messageJSON["records"]:
        attachment = record["attachments"][0]
        date = record["creationTime"]
        parsedDate = parser.parse(date)
        #convert date to file friendly format
        cleanDate = datetime.strftime(parsedDate, "%Y-%m-%d--%H-%M-%S")
        fileExt = getFileExtensionFromMimeType(attachment["contentType"])
        fileName = ("voicemail_recording_%s%s" % (cleanDate, fileExt))
        try:
            #download voicemail using uri link
            res = platform.get(attachment["uri"])
            start = time.time()
            file = open(("%s%s" % (DOWNLOADPATH, fileName)),'wb')
            file.write(res.body())
            file.close()
            end = time.time()
            #prevent too many requests at once
            consumed = end - start
            if consumed < TIMEPERAPICALL:
                time.sleep((TIMEPERAPICALL - consumed)/1000)
        except ApiException as e:
            print(e.message)


#code taken from ringcentral tutorial for selecting file extension
def getFileExtensionFromMimeType(mimeType):
    switcher = {
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/mpeg": ".mp3",
        "audio/ogg": ".ogg"
    }
    return switcher.get(mimeType, ".unknown")

downloadVoiceMails()

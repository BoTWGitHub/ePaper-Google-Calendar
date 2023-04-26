#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function
import datetime
import os.path
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in3g
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

logging.basicConfig(level=logging.DEBUG)

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        logging.info("epd7in3g Demo")

        epd = epd7in3g.EPD()   
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
        
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        
        # Drawing on the image
        logging.info("1.Drawing on the image...")
        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        line = 0
        for event in events:
            data = event['start'].get('dateTime', event['start'].get('date'))+' '+event['summary']
            draw.text((5, line), data, font = font24, fill = epd.BLACK)
            line+=18
            
        epd.display(epd.getbuffer(Himage))
        time.sleep(10)
        
        logging.info("Clear...")
        epd.Clear()
        
        logging.info("Goto Sleep...")
        epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in3g.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    main()

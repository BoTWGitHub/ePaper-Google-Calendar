import os
import logging
import datetime
import platform
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES         = ['https://www.googleapis.com/auth/calendar.readonly']
MAX_EVENTS_NUM = 5

def getGoogleCalendarEvents(eventsList: list):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if platform.system() == "Windows":
        tokenFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config\\token.json')
    else:
        tokenFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/token.json')
    
    if os.path.exists(tokenFilePath):
        creds = Credentials.from_authorized_user_file(tokenFilePath, SCOPES)
    else:
        logging.error(tokenFilePath + ' doesn\'t exist...')
        return

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=MAX_EVENTS_NUM, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        for event in events:
            startDate = event['start'].get('dateTime', event['start'].get('date'))
            eventsList.append([adjustDateStr(startDate), event['summary']])

    except HttpError as error:
        logging.error('An error occurred: %s' % error)

def adjustDateStr(line: str) -> datetime.datetime:
    today = datetime.datetime.now()
    year = today.year
    month = today.month
    day = today.day

    if line.find('T')!=-1:
        line = line[:line.find('T')]

    if line.find('-')!=-1:
        index = line.find('-')
        year = int(line[:index])
        line = line[index+1:]

    if line.find('-')!=-1:
        index = line.find('-')
        month = int(line[:index])
        day = int(line[index+1:])
        return datetime.datetime(year, month, day)
    
    return today

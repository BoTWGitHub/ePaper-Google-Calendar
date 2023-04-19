import os
import datetime
from PIL import Image,ImageDraw,ImageFont
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

MONTHS   = ['Jan.','Feb.','Mar.','Apr.','May.','Jun.','Jul.','Aug.','Sep.','Oct.','Nov.','Dec.']
WEEKDAYS = ['一','二','三','四','五','六','日']

EPD_WIDTH       = 800
EPD_HEIGHT      = 480
BLACK_RGBA  = 0xff000000   #   00  BGR
WHITE_RGBA  = 0xffffffff   #   01
YELLOW_RGBA = 0xff00ffff   #   10
RED_RGBA    = 0xff0000ff   #   11

MAX_LINE     = 5
MAX_LINE_LEN = 684
LINE_START_X = 55
FIRST_LINE_Y = 165
LINE_DIFF_Y  = 48

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def limitLineLength(font, line):
    while font.getlength(line)>MAX_LINE_LEN:
        while font.getlength(line)>(MAX_LINE_LEN-font.getlength('...')):
            line = line[:-1]
        line+='...'
        break
    return line

def adjustDateStr(line: str) -> str:
    if line.find('T')!=-1:
        line = line[:line.find('T')]
    if line.find('-')!=-1:
        line = line[line.find('-')+1:]
    if line.find('-')!=-1:
        index = line.find('-')
        line = line[:index] + '/' + line[index+1:]
    line+=' : '
    return line

def main():
    #init file path and font
    picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'calendar')
    fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
    dinFont = ImageFont.truetype(os.path.join(fontdir, 'DIN Bold.ttf'), 40)
    avantFont = ImageFont.truetype(os.path.join(fontdir, 'Avgardm.ttf'), 50)
    msjhFont = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 40)
    msjhFont36 = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 30)
    helvaticaFont100 = ImageFont.truetype(os.path.join(fontdir, 'helvetica-compressed.ttf'), 100)
    helvaticaFont34 = ImageFont.truetype(os.path.join(fontdir, 'Helvetica-Bold.ttf'), 34)

    #set base image and text image
    Himage = Image.open(os.path.join(picdir, 'Calendar_Sun.bmp')).convert('RGBA')
    TextImage = Image.new('RGBA', (EPD_WIDTH, EPD_HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(TextImage)

    #draw the date onto text image
    date = datetime.datetime.now().date()
    deg = '22'
    draw.text((50, 20), str(date.year), font = dinFont, fill = WHITE_RGBA)
    draw.text((350-avantFont.getlength(MONTHS[date.month-1]), 75), MONTHS[date.month-1], font = avantFont, fill = WHITE_RGBA)
    draw.text((425-helvaticaFont100.getlength(str(date.day))/2, 50), str(date.day), font = helvaticaFont100, fill = YELLOW_RGBA)
    draw.text((500, 80), WEEKDAYS[date.weekday()], font = msjhFont, fill = WHITE_RGBA)
    draw.text((665-helvaticaFont34.getlength(deg), 30), deg, font = helvaticaFont34, fill = WHITE_RGBA)
    draw.text((670, 30), '°', font = helvaticaFont34, fill = RED_RGBA)

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
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=MAX_LINE, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return
        
        lineY = FIRST_LINE_Y
        for event in events:
            startDate = event['start'].get('dateTime', event['start'].get('date'))
            #print(event)
            startDate = adjustDateStr(startDate)
            draw.text((LINE_START_X, lineY), limitLineLength(msjhFont36, startDate+event['summary']), font = msjhFont36, fill = WHITE_RGBA)
            lineY+=LINE_DIFF_Y

    except HttpError as error:
        print('An error occurred: %s' % error)

    #merge base image and text image
    out = Image.alpha_composite(Himage, TextImage)
    out.convert('RGB')
    out.show()

if __name__=='__main__':
    main()

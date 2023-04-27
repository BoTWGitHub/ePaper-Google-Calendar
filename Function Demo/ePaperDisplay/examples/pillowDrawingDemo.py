import os
import json
import enum
import requests
import datetime
from PIL import Image,ImageDraw,ImageFont
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class WeatherType(enum.Enum):
    Sun = 1
    SunAndCloud = 2
    Cloud = 3
    Wind = 4
    Rain = 5

WeatherPicture = {WeatherType.Sun:"Calendar1.bmp"
                  , WeatherType.SunAndCloud:"Calendar2.bmp"
                  , WeatherType.Cloud:"Calendar3.bmp"
                  , WeatherType.Wind:"Calendar4.bmp"
                  , WeatherType.Rain:"Calendar5.bmp"}

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

def getGoogleCalendarEvents() -> list:
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

        return events

    except HttpError as error:
        print('An error occurred: %s' % error)
        return []

def drawCalendarEvents(image, events, font):
    if not events:
            print('No upcoming events found.')
            return
    draw = ImageDraw.Draw(image)
    lineY = FIRST_LINE_Y
    for event in events:
        startDate = event['start'].get('dateTime', event['start'].get('date'))
        #print(event)
        startDate = adjustDateStr(startDate)
        draw.text((LINE_START_X, lineY), limitLineLength(font, startDate+event['summary']), font = font, fill = WHITE_RGBA)
        lineY+=LINE_DIFF_Y

def drawDatetime(image, fonts):
    draw = ImageDraw.Draw(image)

    date = datetime.datetime.now().date()
    
    draw.text((50, 20), str(date.year), font = fonts[0], fill = WHITE_RGBA)
    draw.text((350-fonts[1].getlength(MONTHS[date.month-1]), 75), MONTHS[date.month-1], font = fonts[1], fill = WHITE_RGBA)
    draw.text((425-fonts[2].getlength(str(date.day))/2, 50), str(date.day), font = fonts[2], fill = YELLOW_RGBA)
    draw.text((500, 80), WEEKDAYS[date.weekday()], font = fonts[3], fill = WHITE_RGBA)

def drawWeather(image, font):
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"

    authorization = ""
    location = ""

    cfgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weatherConfig.json')
    if os.path.exists(cfgdir):
        with open(cfgdir, 'r') as configData:
            data = json.loads(configData.read())
            authorization = data["Authorization"]
            location = data["Location"]
    
    params = {
        "Authorization": authorization,
        "locationName": location,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        draw = ImageDraw.Draw(image)
        data = json.loads(response.text)

        weather_elements = data["records"]["location"][0]["weatherElement"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        temp = min_tem + "° - " + max_tem  + "°"
        rain_prob += "%"
        draw.text((668-font.getlength(temp)/2, 114), temp, font = font, fill = WHITE_RGBA)
        draw.text((735, 114), rain_prob, font = font, fill = RED_RGBA)

    else:
        print(response.status_code, " : Can't get data!")

def getWeatherType():
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"

    authorization = ""
    location = ""

    cfgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'weatherConfig.json')
    if os.path.exists(cfgdir):
        with open(cfgdir, 'r') as configData:
            data = json.loads(configData.read())
            authorization = data["Authorization"]
            location = data["Location"]
    
    params = {
        "Authorization": authorization,
        "locationName": location,
    }
    
    type = WeatherType.SunAndCloud

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)

        weather_elements = data["records"]["location"][0]["weatherElement"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        if weather_state.find("雨")!=-1:
            type = WeatherType.Rain
        elif weather_state.find("晴")!=-1 and weather_state.find("雲")!=-1:
            type = WeatherType.SunAndCloud
        elif weather_state.find("風")!=-1:
            type = WeatherType.Wind
        elif weather_state.find("晴")!=-1:
            type = WeatherType.Sun
        elif weather_state.find("雲")!=-1:
            type = WeatherType.Cloud

        return type

    else:
        print(response.status_code, " : Can't get data!")
        return type

def main():
    #init file path and font
    picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'calendar')
    fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
    
    dinFont = ImageFont.truetype(os.path.join(fontdir, 'DIN Bold.ttf'), 40)
    avantFont = ImageFont.truetype(os.path.join(fontdir, 'Avgardm.ttf'), 50)
    msjhFont = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 40)
    msjhFont36 = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 30)
    helvaticaFont100 = ImageFont.truetype(os.path.join(fontdir, 'helvetica-compressed.ttf'), 100)
    helvaticaFont16 = ImageFont.truetype(os.path.join(fontdir, 'Helvetica-Bold.ttf'), 16)

    #set text image
    TextImage = Image.new('RGBA', (EPD_WIDTH, EPD_HEIGHT), (255, 255, 255, 0))

    drawWeather(TextImage, helvaticaFont16)
    drawDatetime(TextImage, [dinFont, avantFont, helvaticaFont100, msjhFont])
    drawCalendarEvents(TextImage, getGoogleCalendarEvents(), msjhFont36)

    #merge base image and text image
    base = Image.open(os.path.join(picdir, WeatherPicture[getWeatherType()])).convert('RGBA')
    out = Image.alpha_composite(base, TextImage)
    out.convert('RGB')
    out.show()

if __name__=='__main__':
    main()

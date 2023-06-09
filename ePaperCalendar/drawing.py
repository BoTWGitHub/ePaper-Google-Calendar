﻿import os
import logging
import weather
import datetime
from PIL import Image,ImageDraw,ImageFont,ImageOps

MONTHS   = ['Jan.','Feb.','Mar.','Apr.','May.','Jun.','Jul.','Aug.','Sep.','Oct.','Nov.','Dec.']
WEEKDAYS = ['一','二','三','四','五','六','日']

BLACK_RGBA  = 0xff000000   #   00  BGR
WHITE_RGBA  = 0xffffffff   #   01
YELLOW_RGBA = 0xff00ffff   #   10
RED_RGBA    = 0xff0000ff   #   11

MAX_LINE_LEN  = 331
LINE_START_X1 = 55
LINE_START_X2 = 420
FIRST_LINE_Y  = 165
LINE_DIFF_Y   = 48

YEAR_POS    = (50, 20)
MONTH_RIGHT = 350
MONTH_TOP   = 75
DAY_CENTER  = 425
DAY_TOP     = 50
WEEKDAY_POS = (500, 80)
TEMP_CENTER = 668
TEMP_TOP    = 114
RAIN_POS    = (735, 114)

NUM_OF_ITEMS = 10

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')

eventFont   = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 30)
yearFont    = ImageFont.truetype(os.path.join(fontdir, 'DIN Bold.ttf'), 40)
monthFont   = ImageFont.truetype(os.path.join(fontdir, 'Avgardm.ttf'), 50)
dayFont     = ImageFont.truetype(os.path.join(fontdir, 'helvetica-compressed.ttf'), 100)
weekdayFont = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 40)
weatherFont = ImageFont.truetype(os.path.join(fontdir, 'Helvetica-Bold.ttf'), 16)
lowBatFont   = ImageFont.truetype(os.path.join(fontdir, 'msjhbd.ttc'), 18)

WeatherPicture = {weather.WeatherType.Sun:"Calendar1.bmp"
                , weather.WeatherType.SunAndCloud:"Calendar2.bmp"
                , weather.WeatherType.Cloud:"Calendar3.bmp"
                , weather.WeatherType.Wind:"Calendar4.bmp"
                , weather.WeatherType.Rain:"Calendar5.bmp"}

class Drawing:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.weatherData = weather.Weather()

    def getNewImage(self, events: list, rotate: bool = False, lowBat: bool = False) -> Image:
        textImage = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))

        self.drawCalendarEvents(textImage, events)
        self.drawDatetime(textImage)
        self.drawWeather(textImage)
        if lowBat:
            self.drawLowBattery(textImage)

        base = Image.open(self.getWeatherBasePic()).convert('RGBA')
        res = Image.alpha_composite(base, textImage)
        res.convert('RGB')

        if rotate:
            logging.info('rotating image...')
            res = res.rotate(180)

        return res

    def drawCalendarEvents(self, image: Image, events: list):
        logging.info("draw list...")
        if not events:
                logging.error('No upcoming events found.')
                return
        
        def limitLineLength(line: str):
            while eventFont.getlength(line)>MAX_LINE_LEN:
                while eventFont.getlength(line)>(MAX_LINE_LEN-eventFont.getlength('...')):
                    line = line[:-1]
                line+='...'
                break
            return line
        draw = ImageDraw.Draw(image)
        lineY = FIRST_LINE_Y
        items = 0
        lineX = LINE_START_X1
        for event in events:
            if items==NUM_OF_ITEMS:
                break
            date = str(event[0].datetime.month) + "/" + str(event[0].datetime.day) + " : "
            eventStr = date + event[1]
            draw.text((lineX, lineY), limitLineLength(eventStr), font = eventFont, fill = WHITE_RGBA)
            lineY+=LINE_DIFF_Y
            items+=1
            if items==5:
                lineX = LINE_START_X2
                lineY = FIRST_LINE_Y

    def drawDatetime(self, image: Image):
        logging.info("draw date time...")
        draw = ImageDraw.Draw(image)

        date = datetime.datetime.now().date()
        draw.text(YEAR_POS, str(date.year), font = yearFont, fill = WHITE_RGBA)
        draw.text((MONTH_RIGHT-monthFont.getlength(MONTHS[date.month-1]), MONTH_TOP), MONTHS[date.month-1], font = monthFont, fill = WHITE_RGBA)
        draw.text((DAY_CENTER-dayFont.getlength(str(date.day))/2, DAY_TOP), str(date.day), font = dayFont, fill = YELLOW_RGBA)
        draw.text(WEEKDAY_POS, WEEKDAYS[date.weekday()], font = weekdayFont, fill = WHITE_RGBA)

    def drawWeather(self, image: Image):
        logging.info("draw weather...")
        draw = ImageDraw.Draw(image)
        
        self.weatherData.fetchWeather()
        data = self.weatherData.getWeather()
        if len(data)<3:
            logging.error('weather data error...')
            return
        
        min_tem = data[0]
        max_tem = data[1]
        rain_prob = data[2]

        temp = min_tem + "° - " + max_tem  + "°"
        rain_prob += "%"
        draw.text((TEMP_CENTER-weatherFont.getlength(temp)/2, TEMP_TOP), temp, font = weatherFont, fill = WHITE_RGBA)
        draw.text(RAIN_POS, rain_prob, font = weatherFont, fill = YELLOW_RGBA)

    def getWeatherBasePic(self) -> str:
        res = os.path.join(picdir, WeatherPicture[self.weatherData.getWeatherType()])
        return res
    
    def drawLowBattery(self, image: Image):
        logging.info("draw low battery...")
        draw = ImageDraw.Draw(image)

        str = "電量不足"
        draw.text((795-lowBatFont.getlength(str), 2), str, font = lowBatFont, fill = RED_RGBA)
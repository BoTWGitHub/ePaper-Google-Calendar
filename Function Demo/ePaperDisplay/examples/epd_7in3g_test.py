#!/usr/bin/python
# -*- coding:utf-8 -*-
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

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in3g Demo")

    epd = epd7in3g.EPD()   
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    # read bmp file 
    logging.info("1.read bmp file")
    logging.info(os.path.join(picdir, '7.3inch-1.bmp'))
    Himage = Image.open(os.path.join(picdir, '7.3inch-1.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)

    logging.info("Goto Sleep...")
    epd.sleep()

    logging.info("2.read bmp file")
    Himage = Image.open(os.path.join(picdir, '7.3inch-2.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)

    logging.info("Goto Sleep...")
    epd.sleep()

    logging.info("3.read bmp file")
    Himage = Image.open(os.path.join(picdir, '7.3inch-3.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)
    
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

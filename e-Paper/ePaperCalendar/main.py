import time
import drawing
import logging
import platform
import googleCalendar
import iCloudCalendar

EPD_WIDTH       = 800
EPD_HEIGHT      = 480

if platform.system() == "Linux":
    from lib.waveshare_epd import epd7in3g

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Running on ' + platform.system())

    eventsList = []
    googleCalendar.getGoogleCalendarEvents(eventsList)
    iCloudCalendar.getiCloudCalendarEvents(eventsList)
    eventsList.sort()
    
    if platform.system() == "Windows":
        image = drawing.Drawing(EPD_WIDTH, EPD_HEIGHT)
        outpurImage = image.getNewImage(eventsList)
        outpurImage.show()
    else:
        try:
            logging.info("ePaperDisplay: epd7in3g")
            epd = epd7in3g.EPD()   
            logging.info("init and Clear")
            epd.init()
            epd.Clear()

            logging.info("get new image...")
            image = drawing.Drawing(epd.width, epd.height)
            outpurImage = image.getNewImage(eventsList)

            logging.info("showing image...")
            epd.display(epd.getbuffer(outpurImage))
            time.sleep(10)

            logging.info("Clear...")
            epd.Clear()

            logging.info("Goto Sleep...")
            epd.sleep()

        except IOError as e:
            logging.info(e)

if __name__=='__main__':
    main()

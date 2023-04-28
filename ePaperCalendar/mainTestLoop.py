import time
import drawing
import logging
import platform
import icsCollect

EPD_WIDTH  = 800
EPD_HEIGHT = 480

if platform.system() == "Linux":
    from lib.waveshare_epd import epd7in3g

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Running on ' + platform.system())
    
    if platform.system() == "Windows":
        logging.info('get calendar data')
        eventsList = icsCollect.collectEvents()
        
        image = drawing.Drawing(EPD_WIDTH, EPD_HEIGHT)
        outpurImage = image.getNewImage(eventsList)
        outpurImage.show()
    else:
        try:
            logging.info("ePaperDisplay: epd7in3g")
            epd = epd7in3g.EPD()   
            logging.info("init display")
            epd.init()

            for _ in range(48):
                logging.info('get calendar data')
                eventsList = icsCollect.collectEvents()

                logging.info("get new image...")
                image = drawing.Drawing(epd.width, epd.height)
                outpurImage = image.getNewImage(eventsList, rotate=True)

                logging.info("showing image...")
                epd.display(epd.getbuffer(outpurImage))
                logging.info("sleep for 1 hour...")
                time.sleep(3600)

            logging.info("Clear...")
            epd.Clear()

            logging.info("Goto Sleep...")
            epd.sleep()

        except IOError as e:
            logging.info(e)

if __name__=='__main__':
    main()

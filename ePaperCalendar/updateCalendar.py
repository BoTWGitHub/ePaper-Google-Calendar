import drawing
import logging
import icsCollect
import getPiSugarBatteryLevel
from lib.waveshare_epd import epd7in3g

def main():
    logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    try:
        logging.info("ePaperDisplay: epd7in3g")
        epd = epd7in3g.EPD()   
        logging.info("init and Clear")
        epd.init()

        lowBattery = False
        if getPiSugarBatteryLevel.waitBatteryData() < 35:
            lowBattery = True

        logging.info("get new image...")
        image = drawing.Drawing(epd.width, epd.height)
        outpurImage = image.getNewImage(icsCollect.collectEvents(), rotate=True, lowBat=lowBattery)

        logging.info("showing image...")
        epd.display(epd.getbuffer(outpurImage))

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

if __name__=='__main__':
    main()

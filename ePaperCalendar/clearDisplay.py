import logging
from lib.waveshare_epd import epd7in3g

def main():
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info("ePaperDisplay: epd7in3g")
        epd = epd7in3g.EPD()

        logging.info("init display")
        epd.init()

        logging.info("Clear...")
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)

if __name__=='__main__':
    main()

import drawing
import logging
import googleCalendar
import iCloudCalendar

EPD_WIDTH       = 800
EPD_HEIGHT      = 480

def main():
    logging.basicConfig(level=logging.INFO)

    eventsList = []
    googleCalendar.getGoogleCalendarEvents(eventsList)
    iCloudCalendar.getiCloudCalendarEvents(eventsList)
    eventsList.sort()
    
    image = drawing.Drawing(EPD_WIDTH, EPD_HEIGHT)
    image.getNewImage(eventsList).show()

if __name__=='__main__':
    main()

from pisugar import *
from datetime import datetime
import logging
import time
import os

def main():
    logging.basicConfig(level=logging.INFO)
    logFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BatteryLog.txt')
    conn, event_conn = connect_tcp('127.0.0.1')
    server = PiSugarServer(conn, event_conn)
    retry = 60 #10min
    while retry>0:
        try:
            level = server.get_battery_level()
            logging.info('get level: ' + str(level))
            break
        except:
            logging.info('not ready...')
            retry-=1
        logging.info('delay 10s...')
        time.sleep(10)
    
    with open(logFilePath, 'a') as file:
        file.write(str(datetime.now()) + ', Battery Level: ' + str(level) + '\n')

if __name__=='__main__':
    main()

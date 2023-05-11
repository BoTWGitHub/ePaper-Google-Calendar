from pisugar import *
from datetime import datetime
import time

def main():
    logFilePath = '/home/k2345777/log.txt'
    conn, event_conn = connect_tcp('127.0.0.1')
    server = PiSugarServer(conn, event_conn)
    retry = 10
    while retry>0:
        try:
            level = server.get_battery_level()
            print(level)
            break
        except:
            print('error...')
            retry-=1
        print('delay 10s...')
        time.sleep(30)
    
    with open(logFilePath, 'w') as file:
        file.write(datetime.now())
        file.write('\n')
        file.write(level)
        file.write('\n')

if __name__=='__main__':
    main()

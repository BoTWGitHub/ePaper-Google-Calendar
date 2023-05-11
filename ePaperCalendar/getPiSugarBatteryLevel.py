from pisugar import *
import time
def main():
    conn, event_conn = connect_tcp('127.0.0.1')
    server = PiSugarServer(conn, event_conn)
    retry = 18
    while retry>0:
        try:
            level = server.get_battery_level()
            print(level)
        except:
            print('error...')
            retry-=1
        print('delay 10s...')
        time.sleep(10)

if __name__=='__main__':
    main()

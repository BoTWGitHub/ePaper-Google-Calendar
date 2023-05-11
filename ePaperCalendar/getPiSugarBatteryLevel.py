from pisugar import *

conn, event_conn = connect_tcp('127.0.0.1')
server = PiSugarServer(conn, event_conn)

level = server.get_battery_level()
print(level)
Project Notes

data-logger-ESP32 is a project to capture time, temperature, and humidity data. An espressif ESP32 microcontroller running micropython executes the data sampling and transmission to a server.  A store and forward approach is used to provide immunity from network connectivity issues.  Battery capacity is a limiting factor.


The RTC DS3231 was set up using setDS3231.py. Run from REPL.

import connect
connect.do_connect()
import setDS3231

Micropython initializes by first reading boot.py, which then calls shell3 and then calls dth.py.


dth.py reads the time from the ds3231 and the temperature  and humidity 
from the AM2302, also known as DHT22, and if networking a available, will
attempt to post the data to a node server.  The code for the server is server.js
The server writes the data to a file named time.json.

A javascript program, named csv.js, reads the time.json file, creates a csv file named 
dth.csv, and optionally deletes the input file. The csv file is used to import into a spreadsheet for charting.

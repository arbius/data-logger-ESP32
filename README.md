Project Notes

data-logger-ESP32 is a project for sensor reading of time, temperature, and humidity.
Using a store and forward approach for the transmission of the data to a server, the system is robust and immune from data loss due to network failures. About 4 Meg of data can be stored. Battery capacity for powering the circuit board is a limitimg factor.

The RTC DS3231 was set up using setDS3231.py. Run from REPL. This is only required to run one time as a battery on the module maintains the time.

Micropython uses a file named boot.py to start the code execution. boot.py calls shell3.py which then calls dth.py.

dth.py reads the time from the ds3231 and the temperature  and humidity 
from the AM2302, also known as DHT22, and if networking a available, will
attempt to post the data to a node server.  The code for the server is server.js
The server writes the data to a file named time.json.

A javascript program, named csv.js, reads the time.json file, creates a csv file named 
dth.csv, and optionally deletes the input file. The csv file is used to import into a spreadsheet for charting.

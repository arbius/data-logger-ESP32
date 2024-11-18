# setDS3231

# Problems connecting with network.
# From REPL, used
# import connect
# connect.mysyntax()
# connect.do_connect()
# import setDS3231
# and it worked

import network
import ntptime
import time
from machine import I2C, Pin
from ds3231 import DS3231

# 1. Connect to Wi-Fi
SSID = 'Galaxy A25 5G 6737'
PASSWORD = '1111111'

# # Set up network credentials
# ssid = "Galaxy A25 5G 6737"
# password = "11111111"


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connected to Wi-Fi:', wlan.ifconfig())

# 2. Get the NTP time and adjust it to your local time
def get_local_time(offset_hours):
    ntptime.settime()  # Get UTC time from NTP server
    utc_time = time.localtime()
    
    # Adjust UTC to local time by adding the time zone offset
    local_time = time.mktime(utc_time) + (offset_hours * 3600) # type: ignore
    return time.localtime(local_time)

# 3. Set local time to the DS3231
def set_ds3231_time(i2c, local_time):
    ds = DS3231(i2c)
    # local_time format: (YYYY, MM, DD, HH, MM, SS, wday, yday)
    ds.set_time(local_time)

# 4. Main Function
def main():
    # Connect to Wi-Fi
    connect_wifi(SSID, PASSWORD)

    # Define I2C bus for DS3231 (adjust SDA and SCL pins as needed)
    i2c = I2C(1, scl=Pin(16), sda=Pin(26))

    # Get the local time, e.g., offset of +2 hours for UTC+2 timezone
    local_time = get_local_time(offset_hours=-7)
    
    # Set the local time to DS3231
    set_ds3231_time(i2c, local_time)

    print("Local time set into DS3231:", local_time)

# Run the main function
main()

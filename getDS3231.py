from machine import I2C, Pin
from ds3231 import *
import time

 
def do_getDS3231():
    sda_pin=Pin(26)
    scl_pin=Pin(16)

    i2c = I2C(scl=scl_pin, sda=sda_pin)
    time.sleep(0.5)

    ds = DS3231(i2c)
    rtc_time = ds.get_time()  # Fetch current date and time from DS3231
    print(rtc_time)
    
    # Print the current date in the format: month/day/year
    print( "Date={}/{}/{}" .format(ds.get_time()[1], ds.get_time()[2],ds.get_time()[0]) )

    # Print the current time in the format: hours:minutes:seconds
    print( "Time={}:{}:{}" .format(ds.get_time()[3], ds.get_time()[4],ds.get_time()[5]) )

    return rtc_time
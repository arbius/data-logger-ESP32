import network
import time
from utime import sleep_ms
from machine import Pin, deepsleep
import dht
import urequests
import ujson
import getDS3231
import sys
import machine
import blink
import os

ON_BOARD_PIN = 25
led_pin = Pin(ON_BOARD_PIN, Pin.OUT)


# Short blinks
SEND_DATA = 2
SOFT_RESET = 3
HARD_RESET = 4
DEEP_SLEEP_RESET = 5
POWER_ON_RESET = 7
UNKNOWN_RESET = 10


# Define reset cause constants
RESET_POWER_ON = machine.PWRON_RESET
RESET_HARDWARE_WATCHDOG = machine.HARD_RESET
RESET_SOFT_RESET = machine.SOFT_RESET
RESET_DEEP_SLEEP = machine.DEEPSLEEP_RESET
RESET_HARD_RESET = machine.HARD_RESET

SLEEP_DURATION = 60 * 1000 * 15 # Sleep for 15 minutes

server_url = "http://Insp16.local:3000/time"
data_file = "unsent_data.json"  # File to store unsent data when Wi-Fi or server is unavailable

# Initialize Wi-Fi connection
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    for _ in range(10):  # Wait up to 10 seconds for Wi-Fi connection
        if wlan.isconnected():
            print("Connected to WiFi:", wlan.ifconfig())
            return wlan
        time.sleep(1)
    
    print("Failed to connect to WiFi.")
    return wlan

# Get time from DS3231 RTC using getDS3231.do_getDS3231 function
def get_rtc_data():
    try:
        dt = getDS3231.do_getDS3231()


        if len(dt) >= 7:  # Ensure the data has the expected number of elements
            year = dt[0]    # Year
            month = dt[1]   # Month
            day = dt[2]     # Day
            hour = dt[3]    # Hour (index 3)
            minute = dt[4]  # Minute
            second = dt[5]  # Second



            print(f"RTC Data: Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}")
            return year, month, day, hour, minute, second
        

        else:
            print("Unexpected RTC data format:", dt)
            return (0, 0, 0, 0, 0, 0)  # Return default values in case of error
    except Exception as e:
        print("Failed to get RTC data:", e)
        return (0, 0, 0, 0, 0, 0)  # Return default values in case of error

# Get temperature and humidity from DHT22
def get_dht22_data():

    # Initialize DHT22 sensor (DHT22 connected to pin 15)
    dht22_sensor = dht.DHT22(Pin(15))

    try:
        dht22_sensor.measure()
        temperature = dht22_sensor.temperature()
        # convert celcius to farenheit
        temperature   = (temperature * 9 / 5) + 32

        humidity = dht22_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Failed to read from DHT22:", e)
        return None, None

# Send data to the Node.js server
def send_data_to_server(data, data_count):
    try:
        # data = ujson.dumps(data)
        if data_count <= 5:
            blink.blink_short(SEND_DATA)

        response = urequests.post(server_url, json=data)
        print("Server response:", response.text)
        response.close()
        return True  # Successfully sent
    except Exception as e:
        print("Failed to send data:", e)
        return False  # Failed to send

# Append unsent data to the local file
def append_unsent_data(data):
    try:
        with open(data_file, "a") as f:
            data = ujson.dumps(data)
            f.write(data + "\n")  # Append each entry on a new line
        print("Data appended to local storage.")
    except Exception as e:
        print("Failed to append data:", e)

# Send stored data from the file to the server
def send_stored_data():
    try:
        with open(data_file, "r") as f:
            lines = f.readlines()
        
        data_count = len(lines)  # Count how many lines (items) need to be sent

        
        for line in lines:
            data = ujson.loads(line.strip())
            print ("send_stored_data", data)

            if send_data_to_server(data, data_count):
                print("Stored data sent successfully!")
                data_count -= 1  # Decrement the count only when the data is successfully sent


            else:
                print("Failed to send stored data.")
                return False # Stop if there's a failure
        return True

    except Exception as e:
        print("Failed to read or send stored data:", e)
        return False
    
def check_if_unsent_data_file_is_empty(data_file):
    try:
        # Check if the file exists
        if data_file in os.listdir():
            # Get the file size
            file_size = os.stat(data_file)[6]
            
            # Return True if the file is empty, False otherwise
            return file_size == 0
        else:
            print('File does not exist.')
            return True  # Consider a non-existent file as empty
    except OSError as e:
        print('Error checking file:', e)
        return True  # If there's an error, treat it as empty


# Main function to collect and send data
def main():

    # Get the current time from the RTC
    year, month, day, hour, minute, second = get_rtc_data()
    dt = get_rtc_data()

    iso_timestamp = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
    

    # Get temperature and humidity from DHT22
    temperature, humidity = get_dht22_data()

    # Prepare data in JSON format
    data = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute, "second": second, "temperature": temperature, "humidity": humidity, "iso_timestamp": iso_timestamp}


    print("Data to be sent:", ujson.dumps(data))

    # Connect to Wi-Fi
    ssid = "Galaxy A25 5G 6737"
    password = "11111111"
    wlan = connect_to_wifi(ssid, password)

    # If Wi-Fi is connected, attempt to send both current and stored data
    if wlan.isconnected():

        # Call the function to check if the file is empty
        if check_if_unsent_data_file_is_empty(data_file):
            print ('unsent_data file is empty')
        else:
            if send_stored_data():  # Try to send any unsent data from previous attempts
                # Clear the file if all data was sent successfully
                with open(data_file, "w") as f:
                    print("Clearing unsent_data.json")
                    f.write("")  # Overwrite the file with an empty string


        # Try sending the current data
        # Second parameter is line count of 1 for single event
        if send_data_to_server(data, 1):
            print("Current data sent successfully!")
        else:
            print("Failed to send current data. Appending to local storage.")
            append_unsent_data(data)
    else:
        print("Wi-Fi not connected, appending data to local storage.")
        append_unsent_data(data)

    # Disconnect Wi-Fi and go to sleep

    print("Disconnecting network")
    wlan.disconnect()
    wlan.active(False)

    # Enter deep sleep for the specified duration
    print(f"Entering deep sleep for {SLEEP_DURATION / 1000} seconds...")
    deepsleep(SLEEP_DURATION)


# Functions to handle reset causes

def handle_power_on_reset():
    print("Power on reset calling main")

    blink.blink_short(POWER_ON_RESET)

    main()    


def handle_hardware_watchdog_reset():
    print("Hardware watchdog reset")
    blink.blink_short(10)

def handle_soft_reset():
    print("Soft reset")
    blink.blink_short(SOFT_RESET)


    print('Enter REPL')
    sys.exit()

def handle_hard_reset():
    print("Hard reset")
    blink.blink_short(HARD_RESET)


    print('Enter REPL')
    sys.exit()
    
# Not available
def handle_brown_out_reset():
    print("Brown-out reset")
    
def handle_deep_sleep_reset():
    print("Deep sleep reset calling main")

    blink.blink_short(DEEP_SLEEP_RESET)

    main()



# Create a dictionary to map reset causes to corresponding handler functions
reset_handlers = {
    RESET_POWER_ON: handle_power_on_reset,
    RESET_HARDWARE_WATCHDOG: handle_hardware_watchdog_reset,
    RESET_HARD_RESET: handle_hard_reset,
    RESET_SOFT_RESET: handle_soft_reset,
    # RESET_BROWN_OUT: handle_brown_out_reset,
    RESET_DEEP_SLEEP: handle_deep_sleep_reset
}


# import machine
# Get the reset cause
reset_cause = machine.reset_cause()

# Clear the reset cause
machine.wake_reason()

# Call the handler function for the reset cause (if defined)
reset_handlers.get(reset_cause, lambda: print("Unknown reset cause"))()

#currently should never reach here
# Clear the reset cause
# machine.wake_reason()

# print('sleeping')

# sleep_ms(10000)


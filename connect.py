import network
import utime
import machine
import config




# Set up network credentials
ssid = "Galaxy A25 5G 6737"
password = "11111111"


def do_connect():

    # import config

    


    utime.sleep(0.1) #  this could be important, recent posting by robert-hh

    # config.wlan.scan()
    print( config.wlan.status())

    if not config.wlan.isconnected():
        print('connecting to network...')
        config.wlan.connect(ssid, password)
        while not config.wlan.isconnected():
                print(config.wlan.status())
                if config.wlan.status()== 201:
                    break
                utime.sleep(1.0) #  this could be important, recent posting by robert-hh


        utime.sleep(1.0) #  this could be important, recent posting by robert-hh

    if not config.wlan.isconnected():
        print('failed connecting to network...')
        print(config.wlan.status())

    
    if  config.wlan.isconnected():
        print(config.wlan.status())

    if config.wlan.status() == network.STAT_GOT_IP:
        print('got it')


        print('network config:', config.wlan.ifconfig())
        print('mac : ', config.wlan.config('mac'))      

    # Get the raw MAC address as a byte string
    mac_byte_string = config.wlan.config('mac')

# Convert the byte string to a human-readable MAC address
    mac_address = ':'.join(['{:02X}'.format(b) for b in mac_byte_string])

# Print the MAC address
    print("MAC address: {}".format(mac_address))

def mysyntax():
    import network

    config.wlan = network.WLAN(network.STA_IF)
    config.wlan.active(True)
    if config.wlan.status() == network.STAT_GOT_IP:
         print('got it')


     
# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

# do_connect()

# machine.deepsleep(5000)


import network

# global wlan

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# wlan.config(reconnects=3)

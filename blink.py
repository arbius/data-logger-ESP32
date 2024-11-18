from machine import Pin
from utime import sleep_ms

ON_BOARD_PIN = 25
led_pin = Pin(ON_BOARD_PIN, Pin.OUT)



def blink_short(short_blinks):
       
        # The more verbose way
        led_pin.value(1)
        sleep_ms(1000)
        for i in range (short_blinks):
            led_pin.value(0)
            sleep_ms(200)
            led_pin.value(1)
            sleep_ms(200)
        
        led_pin.value(0)
        sleep_ms(2000)

        return


# blink_short(5)




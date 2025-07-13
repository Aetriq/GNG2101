# Receiver - Raspberry Pi Pico for #COM 8
from machine import Pin
import utime

rx = Pin(15, Pin.IN)  # Also GP15 (Pin 21)

BIT_DURATION_US = 250



def wait_for_preambule():
    #will wait to see if 1 and 0 alternate 6 times

    count = 0 # will count consecutive alterations
    last = rx.value()
    start_time = utime.ticks_us()

    while utime.ticks_diff(utime.ticks_us(), start_time) < 100000:
        curr = rx.value()
        if curr != last: # so if it alternates
            count+= 1
            last = curr # make sure to update for next round
            utime.sleep_us(BIT_DURATION_US)
            if count >=6: # Verfies amount of alternation
                return True 
            
            else :
                utime.sleep_us(BIT_DURATION_US)

        return False
    

def read_byte():     
    byte = ""
    for i in range(8):
        utime.sleep_us(BIT_DURATION_US)  # Match timing with transmitter
        bit = rx.value()
        #byte |= (bit << i) # type: ignore
        byte += str(bit)
    return byte

while True:
    if wait_for_preambule():
        print("found preambule")
    utime.sleep_us(BIT_DURATION_US)
    value = read_byte()
    print("Received byte:", value)

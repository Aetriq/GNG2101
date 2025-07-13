#COM9
from machine import Pin
import utime

tx = Pin(15, Pin.OUT)
BIT_US = 250  # total bit time (Manchester half = 125 µs)

def send_manchester_bit(bit):
    # 0 = 01, 1 = 10
    if bit == 0:
        tx.value(0)
        utime.sleep_us(BIT_US // 2)
        tx.value(1)
    else:
        tx.value(1)
        utime.sleep_us(BIT_US // 2)
        tx.value(0)
    utime.sleep_us(BIT_US // 2)

def send_byte(byte):
    # Optional: preamble (0xAA = 10101010)
    for _ in range(4):
        send_manchester_bit(1)
        send_manchester_bit(0)

    # Encode each bit as Manchester
    for i in range(8):
        bit = (byte >> (7 - i)) & 1  # MSB first
        send_manchester_bit(bit)

    # Optional: end marker (1)
    send_manchester_bit(1)

# Send 1 through 5 repeatedly
while True:
    led = machine.Pin("LED", machine.Pin.OUT)
    led.off()
    led.on()
    for val in range(1, 6):
        send_byte(val)
        utime.sleep_ms(250)

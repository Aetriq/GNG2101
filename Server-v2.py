import network
import socket
import time
from machine import Pin

SSID = 'GNG2101_Z13_PIANO'
PASSWORD = 'MechanicalCats'

led1 = Pin('GP2',Pin.OUT)

wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.config(essid=SSID, password=PASSWORD)

while not wlan.active():
    pass

print('Access Point created!')
print('SSID:', SSID)
print('IP Address:', wlan.ifconfig()[0])

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('Listening on', addr)

test_value = 1

while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        print("Received request:", request)
        
        response = str(test_value)
        cl.send(response)
        print("Sent:", response)
        led1.toggle()
        test_value = test_value + 1 if test_value < 5 else 1
        
        cl.close()
        time.sleep(0.5)  

    except OSError as e:
        print('Connection error:', e)
        cl.close()
    except Exception as e:
        print('Error:', e)
        cl.close()

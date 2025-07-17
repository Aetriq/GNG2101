import network
import socket
import time
import select
from machine import Pin

SSID = 'GNG2101_Z13_PIANO'
PASSWORD = 'MechanicalCats'

led1 = Pin('GP2', Pin.OUT)
switch = Pin('GP15', Pin.IN, Pin.PULL_UP)  # Pressed = 0

# === Wi-Fi Access Point Setup ===
wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.config(essid=SSID, password=PASSWORD)

while not wlan.active():
    pass

print('Access Point created!')
print('SSID:', SSID)
print('IP Address:', wlan.ifconfig()[0])

# === Socket Setup ===
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
s.setblocking(False)

print('Listening on', addr)

poller = select.poll()
poller.register(s, select.POLLIN)

# === Main Loop ===
while True:
    events = poller.poll(10)

    if events:
        cl = None
        try:
            cl, _ = s.accept()
            cl.settimeout(0.5)
            request = cl.recv(1024)
            response = '2' if switch.value() == 0 else '1'
            cl.send(response.encode())  # Always send bytes!

            print(f"Received request: {request}, Sent: {response}")
            led1.toggle()

        except Exception as e:
            print("Error during client handling:", e)
        finally:
            if cl:
                try:
                    cl.close()
                except Exception as e:
                    print("Error closing client:", e)

            time.sleep(0.01)  # Small delay after closing socket

    else:
        # No incoming connections, do other tasks if needed
        pass

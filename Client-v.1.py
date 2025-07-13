import network
import socket
import time
from machine import reset, Pin

AP_SSID = 'GNG2101_Z13_PIANO'
AP_PASSWORD = 'MechanicalCats'
AP_IP = '192.168.4.1'

led1 = Pin('GP2',Pin.OUT)

def connect_to_ap():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    wlan.disconnect()
    time.sleep(0.1)
    
    print(f"Connecting to {AP_SSID}")
    wlan.connect(AP_SSID, AP_PASSWORD)

    max_wait = 15
    start_time = time.time()
    
    while not wlan.isconnected():
        status = wlan.status()
        if status < 0 or time.time() - start_time > max_wait:
            print(f"Connection failed! Status: {status}")
            return None
        print(f"Status: {status}, waiting...")
        time.sleep(0.1)
    
    print('Connected! IP:', wlan.ifconfig()[0])
    return wlan

wlan = None
while wlan is None:
    wlan = connect_to_ap()
    if wlan is None:
        print("Retrying connection in 3 seconds...")
        time.sleep(3)

print("Connecting to server...")

while True:
    try:
        s = socket.socket()
        s.settimeout(5.0)  
        
        s.connect((AP_IP, 80))
        s.send(b"GET Data")
        
        data = s.recv(512).decode().strip()
        print("Status: Connected. Packet received:", data)
        led1.toggle()
        
    except OSError as e:
        print("Socket error:", e)
    # Optimize performance by bypassing ValueError
    # except ValueError:
    #   print("Parse error - Received:", data)
    finally:
        s.close()
        time.sleep(1)  
import network
import socket
import time
import gc

from machine import reset, Pin, PWM

AP_SSID = 'GNG2101_Z13_PIANO'
AP_PASSWORD = 'MechanicalCats'
AP_IP = '192.168.4.1'

led1 = Pin('GP2', Pin.OUT)  # Existing LED (heartbeat or activity)

# === New Components ===
indicator_led = Pin('GP10', Pin.OUT)  # Status indicator LED
servo_pwm = PWM(Pin('GP12'))          # Servo motor on GP12
servo_pwm.freq(50)                    # Standard servo frequency 50Hz

# --- Helper: Convert angle to duty for 0° to 180° ---
def set_servo_angle(angle):
    # Convert angle to duty cycle between 1ms (0°) and 2ms (180°)
    min_duty = 1000  # in microseconds
    max_duty = 2000
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo_pwm.duty_u16(int(duty * 65535 / 20000))  # 20ms period (50Hz)
    
# --- Indicator Patterns ---
def blink_led(delay_ms, count=1):
    for _ in range(count):
        indicator_led.on()
        time.sleep_ms(delay_ms)
        indicator_led.off()
        time.sleep_ms(delay_ms)

def show_connecting_status():
    blink_led(500)  # Just blink once; logic happens in loop

def show_connected_status():
    indicator_led.on()  # Solid ON

def show_connection_failed_status():
    for _ in range(5):  # Rapid blink for connection fail
        blink_led(100)

def show_other_error_status():
    blink_led(100, 2)  # 2 quick blinks

# --- Wi-Fi Connection ---
def connect_to_ap():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.disconnect()
    time.sleep(0.1)

    print(f"Connecting to {AP_SSID}")
    wlan.connect(AP_SSID, AP_PASSWORD)

    max_wait = 15
    start_time = time.time()

    # --- Setup for non-blocking blink ---
    last_blink = time.ticks_ms()
    led_state = False
    blink_interval = 500  # Medium blink (500ms)

    while not wlan.isconnected():
        status = wlan.status()
        if status < 0 or time.time() - start_time > max_wait:
            print(f"Connection failed! Status: {status}")
            indicator_led.off()
            return None
        print(f"Status: {status}, waiting...")

        # Non-blocking LED blink logic
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_blink) >= blink_interval:
            led_state = not led_state
            indicator_led.value(led_state)
            last_blink = current_time

        time.sleep(0.05)  # Short sleep to allow Wi-Fi polling and blinking

    print('Connected! IP:', wlan.ifconfig()[0])
    indicator_led.on()  # Solid ON when connected
    return wlan


# --- Initial Connection Attempt ---
wlan = None
while wlan is None:
    show_connecting_status()  # Blink to indicate attempt
    wlan = connect_to_ap()
    if wlan is None:
        show_connection_failed_status()  # Blink rapidly on fail
        print("Retrying connection in 3 seconds...")
        time.sleep(3)

show_connected_status()
print("Connecting to server...")


# --- Main Loop ---
while True:
    try:
        s = socket.socket()
        s.settimeout(5.0)

        s.connect((AP_IP, 80))
        s.send(b"GET Data")

        gc.collect()

        data = s.recv(512).decode().strip()
        print("Status: Connected. Packet received:", data)
        led1.toggle()

        # === Servo Control ===
        if data == '1':
            set_servo_angle(0)
        elif data == '2':
            set_servo_angle(70)

    except OSError as e:
        print("Socket error:", e)
        show_other_error_status()
    finally:
        s.close()
        time.sleep(0.02)

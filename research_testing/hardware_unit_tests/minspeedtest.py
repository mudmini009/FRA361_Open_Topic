# minspeedtest.py
import threading, time, serial, keyboard
from config import SERIAL_PORT, SERIAL_BAUD

# ─── Setup Serial ─────────────────────────────────
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
time.sleep(2)
print(f"[+] Opened {SERIAL_PORT}@{SERIAL_BAUD}")

# ─── Shared state ─────────────────────────────────
speeds      = [30, 30, 30, 30]           # [FL, FR, BL, BR]
wheel_names = ['Front-Left', 'Front-Right', 'Back-Left', 'Back-Right']
selected    = 0
stop_flag   = False

print("Controls: Z=cycle wheel, C=+1 PWM, X=-1 PWM, ESC=quit")
print(f"Selected → {wheel_names[selected]} = {speeds[selected]}")

# ─── Sender thread ────────────────────────────────
def sender_loop():
    """Continuously send the latest speeds at 20 Hz."""
    while not stop_flag:
        msg = "{},{},{},{}\n".format(*speeds)
        ser.write(msg.encode('utf-8'))
        print("→ sent:", msg.strip())
        time.sleep(0.05)  # 20 Hz

thread = threading.Thread(target=sender_loop, daemon=True)
thread.start()

# ─── Key‐handling loop ────────────────────────────
last = {'z': False, 'c': False, 'x': False}
try:
    while True:
        # Cycle selected wheel on Z press
        z = keyboard.is_pressed('z')
        if z and not last['z']:
            selected = (selected + 1) % 4
            print(f"Selected → {wheel_names[selected]} = {speeds[selected]}")
        last['z'] = z

        # Increase PWM on C
        c = keyboard.is_pressed('c')
        if c and not last['c']:
            speeds[selected] += 1
            print(f"{wheel_names[selected]} PWM → {speeds[selected]}")
        last['c'] = c

        # Decrease PWM on X
        x = keyboard.is_pressed('x')
        if x and not last['x']:
            speeds[selected] -= 1
            print(f"{wheel_names[selected]} PWM → {speeds[selected]}")
        last['x'] = x

        # Quit on ESC
        if keyboard.is_pressed('esc'):
            print("Exiting…")
            break

        time.sleep(0.01)  # small debounce

finally:
    # signal sender to stop, wait a moment, then clean up
    stop_flag = True
    thread.join(0.1)
    ser.close()
    print("Serial closed.")

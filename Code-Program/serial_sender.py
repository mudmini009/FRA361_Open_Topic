#send serail to esp32
# serial_sender.py
import time
import serial
from serial.tools import list_ports
from config import SERIAL_PORT, SERIAL_BAUD

class SerialSender:
    def __init__(self):
        ports = [p.device for p in list_ports.comports()]
        print("Available serial ports:", ports)
        try:
            self.ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
            time.sleep(2)
            print(f"Opened serial port {SERIAL_PORT}@{SERIAL_BAUD}")
            self.enabled = True
        except Exception as e:
            print(f"⚠️ Could not open port {SERIAL_PORT}: {e}")
            print("→ Continuing without serial output.")
            self.enabled = False

    def send(self, data):
        if not self.enabled:
            return
        msg = "{:.1f},{:.1f},{:d},{:d}\n".format(*data)
        self.ser.write(msg.encode('utf-8'))
        # ← New line: echo so you know it went out
        print("→ sent:", msg.strip())

    def close(self):
        if self.enabled:
            self.ser.close()
# test_latency.py

import time
import pyautogui
from serial_sender import SerialSender

# ─── Configuration ────────────────────────────────────
TEST_COUNT = 10            # number of trials per direction
SPEED      = 70            # wheel % impulse (±)
THRESHOLD  = 5             # px cursor must move to register
PAUSE      = 1.0           # seconds between trials

# ─── Helper: wait for cursor to move THRESHOLD px from y0 ───
def wait_for_movement(y0, direction):
    """
    Block until cursor has moved by THRESHOLD px in 'up' or 'down' dir.
    """
    while True:
        _, y = pyautogui.position()
        dy = y - y0
        if direction == 'up'   and dy <= -THRESHOLD:
            return
        if direction == 'down' and dy >=  THRESHOLD:
            return
        time.sleep(0.001)

# ─── Run one batch of discrete‐pulse tests ─────────────────
def run_tests(direction, sender):
    latencies = []
    for i in range(1, TEST_COUNT+1):
        # sample baseline cursor Y
        _, y0 = pyautogui.position()

        # 1) send single impulse
        pwm =  SPEED if direction=='up' else -SPEED
        sender.send_wheels(pwm,pwm,pwm,pwm)

        # 2) record send timestamp
        t0 = time.time()

        # 3) immediately stop wheels
        sender.send_wheels(0,0,0,0)

        # 4) wait for cursor move
        wait_for_movement(y0, direction)
        latency = (time.time() - t0)*1000
        latencies.append(latency)
        print(f"[{direction.upper()} #{i}] {latency:.1f} ms")

        # rest before next trial
        time.sleep(PAUSE)

    return latencies

# ─── Main ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Hardware→Mouse latency test (discrete pulses)")
    sender = SerialSender()
    if not sender.enabled:
        print("Serial port unavailable, aborting.")
        exit(1)

    print("Get your cursor on a blank area. Starting in 3s…")
    time.sleep(3)

    up_lat   = run_tests('up',   sender)
    down_lat = run_tests('down', sender)

    sender.close()

    print("\n=== LATENCY RESULTS ===")
    print("Up    ms:", [f"{l:.1f}" for l in up_lat])
    print("Down  ms:", [f"{l:.1f}" for l in down_lat])
    print(f"Avg Up:   {sum(up_lat)/len(up_lat):.1f} ms")
    print(f"Avg Down: {sum(down_lat)/len(down_lat):.1f} ms")

#data logging
# logger.py
import csv

class DataLogger:
    def __init__(self):
        self.entries = []  # list of (dx, dy, mode)

    def log(self, dx, dy, mode):
        """Append one sample."""
        self.entries.append((dx, dy, mode))

    def save_csv(self, filename="aimbot_log.csv"):
        """Save all entries to CSV."""
        with open(filename, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["dx", "dy", "mode"])
            w.writerows(self.entries)
        print(f"✅ Saved log to {filename}")

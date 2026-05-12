# logger.py — Per-frame data logging to CSV
import csv
from typing import List, Tuple


class DataLogger:
    """Accumulates (dx, dy, mode) samples and writes them to disk."""

    def __init__(self) -> None:
        self.entries: List[Tuple[float, float, int]] = []

    def log(self, dx: float, dy: float, mode: int) -> None:
        """Append one sample."""
        self.entries.append((dx, dy, mode))

    def save_csv(self, filename: str = "aimbot_log.csv") -> None:
        """Flush all entries to a CSV file."""
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["dx", "dy", "mode"])
            writer.writerows(self.entries)
        print(f"✅ Saved {len(self.entries)} samples → {filename}")

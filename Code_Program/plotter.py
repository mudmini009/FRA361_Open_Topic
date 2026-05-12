# plotter.py — Post-session matplotlib plots
from typing import List, Tuple

import matplotlib.pyplot as plt


def plot_log(entries: List[Tuple[float, float, int]]) -> None:
    """
    Show a 3-row chart (mode / dx / dy) vs. frame index.

    Called automatically when the aimbot exits.
    """
    if not entries:
        print("No data to plot.")
        return

    frames = range(len(entries))
    dxs    = [e[0] for e in entries]
    dys    = [e[1] for e in entries]
    modes  = [e[2] for e in entries]

    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(10, 6))

    axes[0].plot(frames, modes, marker="o", markersize=2, linestyle="-")
    axes[0].set_ylabel("Mode")
    axes[0].set_title("Aimbot Session Log")

    axes[1].plot(frames, dxs, marker=".", markersize=1, linestyle="-")
    axes[1].set_ylabel("dx (px)")

    axes[2].plot(frames, dys, marker=".", markersize=1, linestyle="-")
    axes[2].set_ylabel("dy (px)")
    axes[2].set_xlabel("Frame #")

    plt.tight_layout()
    plt.show()

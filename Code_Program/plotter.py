# plotter.py
import matplotlib.pyplot as plt

def plot_log(entries):
    """
    entries: list of (dx, dy, mode)
    Produces a 3‐row plot: mode, dx, dy vs frame index.
    """
    xs   = list(range(len(entries)))
    dxs  = [e[0] for e in entries]
    dys  = [e[1] for e in entries]
    modes= [e[2] for e in entries]

    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(8, 6))

    axs[0].plot(xs, modes,   marker="o", linestyle="-")
    axs[0].set_ylabel("mode")
    axs[0].set_title("Aimbot Data Log")

    axs[1].plot(xs, dxs,     marker=".", linestyle="-")
    axs[1].set_ylabel("dx (px)")

    axs[2].plot(xs, dys,     marker=".", linestyle="-")
    axs[2].set_ylabel("dy (px)")
    axs[2].set_xlabel("frame #")

    plt.tight_layout()
    plt.show()

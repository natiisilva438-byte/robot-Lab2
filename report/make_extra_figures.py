"""Regenerate the analytical Lab 2 figures used in the report."""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


out = Path(__file__).parent
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})


def box(ax, xy, width, height, label, facecolor):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), width, height, boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=0.9, edgecolor="#334155", facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, label, ha="center", va="center", fontsize=7.5)


def arrow(ax, start, end, color="#475569"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11,
                                 linewidth=1.2, color=color))


fig, ax = plt.subplots(figsize=(4.1, 2.5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
box(ax, (0.37, 0.75), 0.26, 0.16, "world", "#e2e8f0")
box(ax, (0.08, 0.43), 0.29, 0.16, "av1", "#dbeafe")
box(ax, (0.63, 0.43), 0.29, 0.16, "av2", "#ffedd5")
arrow(ax, (0.43, 0.75), (0.25, 0.60), "#2563eb")
arrow(ax, (0.57, 0.75), (0.75, 0.60), "#ea580c")
ax.text(0.24, 0.69, r"$^wT_1$", color="#2563eb", ha="center")
ax.text(0.76, 0.69, r"$^wT_2$", color="#ea580c", ha="center")
box(ax, (0.25, 0.09), 0.50, 0.16, "plots publisher  /visuals", "#dcfce7")
arrow(ax, (0.25, 0.43), (0.40, 0.26))
arrow(ax, (0.75, 0.43), (0.60, 0.26))
ax.text(0.50, 0.35, "2 meshes + 3 trails", ha="center", va="center", fontsize=7)
ax.text(0.5, 0.98, "dynamic: /tf     static: /tf_static", ha="center", va="top", fontsize=7.5)
fig.tight_layout(pad=0.15)
fig.savefig(out / "tf_graph.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)

t = np.linspace(0, 2 * np.pi, 500)
av1 = np.column_stack((np.cos(t), np.sin(t), np.zeros_like(t)))
av2 = np.column_stack((np.sin(t), np.zeros_like(t), np.cos(2 * t)))
snapshot = np.pi / 4
p1 = np.array([np.cos(snapshot), np.sin(snapshot), 0.0])
p2 = np.array([np.sin(snapshot), 0.0, np.cos(2 * snapshot)])

fig = plt.figure(figsize=(4.1, 3.0))
ax = fig.add_subplot(111, projection="3d")
ax.plot(*av1.T, color="#2563eb", linewidth=2, label="AV1 circle")
ax.plot(*av2.T, color="#ea580c", linewidth=2, label="AV2 parabola")
ax.scatter(*p1, color="#2563eb", s=34, depthshade=False)
ax.scatter(*p2, color="#ea580c", s=34, depthshade=False)
ax.plot(*np.vstack((p1, p2)).T, color="#475569", linestyle="--", linewidth=1)
ax.set(xlabel="world x", ylabel="world y", zlabel="world z",
       xlim=(-1.1, 1.1), ylim=(-1.1, 1.1), zlim=(-1.1, 1.1))
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=23, azim=-57)
ax.legend(loc="upper left", fontsize=7, frameon=False)
fig.tight_layout(pad=0.2)
fig.savefig(out / "world_3d.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)

labels = ["World parabola", "Relative plane", "Relative ellipse"]
noetic = np.array([2.22044605e-16, 4.44089210e-16, 1.77635684e-15])
humble = np.array([1.94289029e-16, 4.44089210e-16, 9.99200722e-16])
positions = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(4.1, 2.25))
ax.scatter(-np.log10(noetic), positions - 0.11, color="#2563eb", s=52,
           marker="o", label="ROS 1 Noetic", zorder=3)
ax.scatter(-np.log10(humble), positions + 0.11, color="#ea580c", s=52,
           marker="s", label="ROS 2 Humble", zorder=3)
ax.set_yticks(positions, labels)
ax.invert_yaxis()
ax.set_xlim(14.45, 16.0)
ax.set_xlabel(r"$-\log_{10}$(maximum absolute residual)")
ax.grid(axis="x", color="#cbd5e1", linewidth=0.7)
ax.set_axisbelow(True)
ax.legend(loc="lower right", fontsize=7, frameon=False)
fig.tight_layout(pad=0.3)
fig.savefig(out / "precision.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)

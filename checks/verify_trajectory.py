"""Numerical checks for the Lab 2 relative-pose derivation and report figure."""
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def coordinates(t):
    c, s = np.cos(t), np.sin(t)
    av1 = np.column_stack((c, s, np.zeros_like(t)))
    av2 = np.column_stack((s, np.zeros_like(t), np.cos(2 * t)))
    delta = av2 - av1
    relative = np.column_stack((c * delta[:, 0] + s * delta[:, 1],
                                -s * delta[:, 0] + c * delta[:, 1],
                                delta[:, 2]))
    return av1, av2, relative


def main():
    t = np.linspace(0, 2 * math.pi, 1001)
    av1, av2, relative = coordinates(t)
    expected = np.column_stack((np.sin(2 * t) / 2 - 1,
                                -np.sin(t) ** 2,
                                np.cos(2 * t)))
    assert np.allclose(relative, expected, atol=1e-12)
    assert np.max(np.abs(relative[:, 2] - 2 * relative[:, 1] - 1)) < 1e-12
    xp = relative[:, 0] + 1
    yp = (relative[:, 1] + .5 + 2 * relative[:, 2]) / math.sqrt(5)
    assert np.max(np.abs((xp / .5) ** 2 + (yp / (math.sqrt(5) / 2)) ** 2 - 1)) < 1e-12

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    axes[0].plot(av1[:, 0], av1[:, 1], label="AV1 in world", lw=2)
    axes[0].plot(av2[:, 0], av2[:, 2], label="AV2 in world (x-z)", lw=2)
    axes[0].set_aspect("equal")
    axes[0].set_xlabel("horizontal coordinate")
    axes[0].set_ylabel("vertical coordinate")
    axes[0].grid(alpha=.25)
    axes[0].legend(fontsize=8)
    axes[1].plot(xp, yp, color="#c85b36", lw=2)
    axes[1].set_aspect("equal")
    axes[1].set_xlabel(r"$x_p$")
    axes[1].set_ylabel(r"$y_p$")
    axes[1].grid(alpha=.25)
    axes[1].set_title("AV2 relative to AV1")
    fig.tight_layout()
    output = Path(__file__).resolve().parents[1] / "report" / "trajectories.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220)
    print("PASS: transform, plane, and ellipse identities; saved", output)


if __name__ == "__main__":
    main()

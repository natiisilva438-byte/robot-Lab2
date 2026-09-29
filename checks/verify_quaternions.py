"""Independent numerical checks of the quaternion matrix identities."""
import numpy as np


def omega1(q):
    a, b, c, d = q
    return np.array([[d, -c, b, a], [c, d, -a, b],
                     [-b, a, d, c], [-a, -b, -c, d]])


def omega2(q):
    a, b, c, d = q
    return np.array([[d, c, -b, a], [-c, d, a, b],
                     [b, -a, d, c], [-a, -b, -c, d]])


def main():
    rng = np.random.default_rng(2023)
    unit = np.eye(4)
    identity_quaternion = np.array([0., 0., 0., 1.])
    for _ in range(1000):
        q, x, y = rng.normal(size=(3, 4))
        q /= np.linalg.norm(q)
        for omega in (omega1, omega2):
            matrix = omega(q)
            assert np.allclose(matrix.T @ matrix, unit, atol=1e-12)
            assert np.allclose(matrix.T @ q, identity_quaternion, atol=1e-12)
        assert np.allclose(omega1(x) @ omega2(y), omega2(y) @ omega1(x), atol=1e-12)
        assert np.allclose(omega1(x) @ omega2(y).T,
                           omega2(y).T @ omega1(x), atol=1e-12)
    print("PASS: quaternion identities for 1000 deterministic samples")


if __name__ == "__main__":
    main()

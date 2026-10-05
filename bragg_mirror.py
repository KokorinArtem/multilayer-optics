import numpy as np
import matplotlib.pyplot as plt


# Refractive indices
n_air = 1.0
n_sio2 = 1.46
n_tio2 = 2.40
n_glass = 1.50

# Design wavelength
lambda0 = 550e-9

# Quarter-wave thicknesses
d_sio2 = lambda0 / (4 * n_sio2)
d_tio2 = lambda0 / (4 * n_tio2)

print(f"SiO2 thickness: {d_sio2 * 1e9:.2f} nm")
print(f"TiO2 thickness: {d_tio2 * 1e9:.2f} nm")


def layer_matrix(n, d, wavelength):
    delta = 2 * np.pi * n * d / wavelength

    return np.array([
        [np.cos(delta), 1j * np.sin(delta) / n],
        [1j * n * np.sin(delta), np.cos(delta)]
    ])


def reflectance_dbr(wavelength, pairs):
    M = np.identity(2, dtype=complex)

    for _ in range(pairs):
        M_sio2 = layer_matrix(n_sio2, d_sio2, wavelength)
        M_tio2 = layer_matrix(n_tio2, d_tio2, wavelength)

        M = M @ M_sio2 @ M_tio2

    A = M[0, 0]
    B = M[0, 1]
    C = M[1, 0]
    D = M[1, 1]

    numerator = (
        n_air * A
        + n_air * n_glass * B
        - C
        - n_glass * D
    )

    denominator = (
        n_air * A
        + n_air * n_glass * B
        + C
        + n_glass * D
    )

    r = numerator / denominator

    return abs(r) ** 2


# Wavelength range
wavelengths = np.linspace(350e-9, 800e-9, 1000)

# Number of SiO2/TiO2 pairs
pair_numbers = [1, 3, 5, 10]

plt.figure(figsize=(10, 6))

for pairs in pair_numbers:

    R = []

    for wavelength in wavelengths:
        R.append(reflectance_dbr(wavelength, pairs))

    plt.plot(
        wavelengths * 1e9,
        R,
        label=f"N = {pairs}"
    )


# Design wavelength
plt.axvline(
    lambda0 * 1e9,
    linestyle="--",
    label="Design wavelength = 550 nm"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance R")

plt.title(
    "Distributed Bragg Reflector: "
    "(SiO2 / TiO2)^N"
)

plt.grid()
plt.legend()

plt.savefig(
    "figures/bragg_mirror.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
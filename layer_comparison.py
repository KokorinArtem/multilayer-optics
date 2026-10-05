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


def layer_matrix(n, d, wavelength):
    delta = 2 * np.pi * n * d / wavelength

    return np.array([
        [np.cos(delta), 1j * np.sin(delta) / n],
        [1j * n * np.sin(delta), np.cos(delta)]
    ])


def multilayer_reflectance(layers, wavelength):
    # Start with identity matrix
    M = np.identity(2, dtype=complex)

    # Multiply matrices of all layers
    for n, d in layers:
        M = M @ layer_matrix(n, d, wavelength)

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

    return np.abs(r) ** 2


# Structures
structure_1 = [
    (n_sio2, d_sio2),
    (n_tio2, d_tio2)
]

structure_2 = [
    (n_tio2, d_tio2),
    (n_sio2, d_sio2)
]

structure_3 = [
    (n_sio2, d_sio2),
    (n_tio2, d_tio2),
    (n_sio2, d_sio2),
    (n_tio2, d_tio2),
    (n_sio2, d_sio2),
    (n_tio2, d_tio2)
]

# Wavelength range
wavelengths_nm = np.linspace(350, 800, 1000)
wavelengths = wavelengths_nm * 1e-9

# Calculate spectra
R1 = np.array([
    multilayer_reflectance(structure_1, wavelength)
    for wavelength in wavelengths
])

R2 = np.array([
    multilayer_reflectance(structure_2, wavelength)
    for wavelength in wavelengths
])

R3 = np.array([
    multilayer_reflectance(structure_3, wavelength)
    for wavelength in wavelengths
])

# Bare glass
R_glass = ((n_air - n_glass) / (n_air + n_glass)) ** 2

# Reflectance exactly at 550 nm
R1_550 = multilayer_reflectance(structure_1, lambda0)
R2_550 = multilayer_reflectance(structure_2, lambda0)
R3_550 = multilayer_reflectance(structure_3, lambda0)

print("Reflectance at 550 nm:")
print(f"Bare glass: {R_glass * 100:.2f}%")
print(f"SiO2 / TiO2: {R1_550 * 100:.2f}%")
print(f"TiO2 / SiO2: {R2_550 * 100:.2f}%")
print(f"(SiO2 / TiO2) x3: {R3_550 * 100:.2f}%")

# Plot
plt.figure(figsize=(10, 6))

plt.plot(
    wavelengths_nm,
    R1,
    label="SiO2 / TiO2"
)

plt.plot(
    wavelengths_nm,
    R2,
    label="TiO2 / SiO2"
)

plt.plot(
    wavelengths_nm,
    R3,
    label="(SiO2 / TiO2) x3"
)

plt.axhline(
    R_glass,
    linestyle="--",
    label="Bare glass"
)

plt.axvline(
    550,
    linestyle="--",
    label="550 nm"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance R")

plt.title(
    "Effect of Layer Order and Number on Reflectance"
)

plt.grid()
plt.legend()
plt.savefig("figures/layer_comparison.png", dpi=300, bbox_inches="tight")
plt.show()
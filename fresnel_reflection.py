import numpy as np
import matplotlib.pyplot as plt

# Refractive indices
n_air = 1.0
n_sio2 = 1.46
n_tio2 = 2.40
n_glass = 1.50

# Design wavelength (meters)
lambda0 = 550e-9

# Quarter-wave layer thicknesses
d_sio2 = lambda0 / (4 * n_sio2)
d_tio2 = lambda0 / (4 * n_tio2)

print(f"SiO2 thickness: {d_sio2 * 1e9:.2f} nm")
print(f"TiO2 thickness: {d_tio2 * 1e9:.2f} nm")


def layer_matrix(n, d, wavelength):
    """
    Transfer matrix of one optical layer
    at normal incidence.
    """

    delta = 2 * np.pi * n * d / wavelength

    return np.array([
        [np.cos(delta), 1j * np.sin(delta) / n],
        [1j * n * np.sin(delta), np.cos(delta)]
    ])


def reflectance(wavelength):

    # Matrix for SiO2
    M1 = layer_matrix(
        n_sio2,
        d_sio2,
        wavelength
    )

    # Matrix for TiO2
    M2 = layer_matrix(
        n_tio2,
        d_tio2,
        wavelength
    )

    # Total matrix
    M = M1 @ M2

    # Elements of matrix
    A = M[0, 0]
    B = M[0, 1]
    C = M[1, 0]
    D = M[1, 1]

    # Reflection amplitude
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


# Wavelength range: 350–800 nm
wavelengths_nm = np.linspace(350, 800, 1000)
wavelengths = wavelengths_nm * 1e-9

R = np.array([
    reflectance(wavelength)
    for wavelength in wavelengths
])

# Reflection of bare glass for comparison
R_bare_glass = (
    (n_air - n_glass)
    / (n_air + n_glass)
) ** 2

print(f"Bare glass reflectance: {R_bare_glass:.4f}")

# Plot
plt.figure(figsize=(10, 6))

plt.plot(
    wavelengths_nm,
    R,
    label="Air → SiO2 → TiO2 → Glass"
)

plt.axhline(
    R_bare_glass,
    linestyle="--",
    label="Bare glass"
)

plt.axvline(
    lambda0 * 1e9,
    linestyle="--",
    label="Design wavelength = 550 nm"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance R")

plt.title(
    "Reflectance of a Two-Layer Optical Structure"
)

plt.grid()
plt.legend()

plt.show()
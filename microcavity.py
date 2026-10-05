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

# Defect layer
n_defect = n_sio2

# Half-wave defect thickness
d_defect = lambda0 / (2 * n_defect)

# Number of Bragg pairs on each side
pairs = 5


def layer_matrix(n, d, wavelength):
    delta = 2 * np.pi * n * d / wavelength

    return np.array([
        [
            np.cos(delta),
            1j * np.sin(delta) / n
        ],
        [
            1j * n * np.sin(delta),
            np.cos(delta)
        ]
    ])


def calculate_reflectance(M):
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


def bragg_mirror(wavelength):
    M = np.identity(2, dtype=complex)

    for _ in range(pairs):

        M = (
            M
            @ layer_matrix(
                n_sio2,
                d_sio2,
                wavelength
            )
            @ layer_matrix(
                n_tio2,
                d_tio2,
                wavelength
            )
        )

    return M


def microcavity(wavelength):
    M = np.identity(2, dtype=complex)

    # Left Bragg mirror
    for _ in range(pairs):

        M = (
            M
            @ layer_matrix(
                n_sio2,
                d_sio2,
                wavelength
            )
            @ layer_matrix(
                n_tio2,
                d_tio2,
                wavelength
            )
        )

    # Defect layer
    M = (
        M
        @ layer_matrix(
            n_defect,
            d_defect,
            wavelength
        )
    )

    # Right Bragg mirror
    # Reverse layer order
    for _ in range(pairs):

        M = (
            M
            @ layer_matrix(
                n_tio2,
                d_tio2,
                wavelength
            )
            @ layer_matrix(
                n_sio2,
                d_sio2,
                wavelength
            )
        )

    return M


# Wavelength range
wavelengths = np.linspace(
    400e-9,
    700e-9,
    3000
)

R_bragg = []
R_cavity = []

for wavelength in wavelengths:

    M_bragg = bragg_mirror(wavelength)
    M_cavity = microcavity(wavelength)

    R_bragg.append(
        calculate_reflectance(M_bragg)
    )

    R_cavity.append(
        calculate_reflectance(M_cavity)
    )


# Find minimum reflectance near the design wavelength
R_cavity_array = np.array(R_cavity)

region = (
    (wavelengths > 500e-9)
    & (wavelengths < 600e-9)
)

indices = np.where(region)[0]

minimum_index = indices[
    np.argmin(R_cavity_array[region])
]

resonance_wavelength = (
    wavelengths[minimum_index]
)

minimum_reflectance = (
    R_cavity_array[minimum_index]
)


print(
    f"Design wavelength: "
    f"{lambda0 * 1e9:.1f} nm"
)

print(
    f"Defect thickness: "
    f"{d_defect * 1e9:.2f} nm"
)

print(
    f"Resonance wavelength: "
    f"{resonance_wavelength * 1e9:.2f} nm"
)

print(
    f"Minimum reflectance: "
    f"{minimum_reflectance:.6f}"
)


# Plot
plt.figure(figsize=(10, 6))

plt.plot(
    wavelengths * 1e9,
    R_bragg,
    label="Bragg mirror"
)

plt.plot(
    wavelengths * 1e9,
    R_cavity,
    label="Microcavity with defect"
)

plt.axvline(
    lambda0 * 1e9,
    linestyle="--",
    label="Design wavelength = 550 nm"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance R")

plt.title(
    "Defect Mode in a Bragg Microcavity"
)

plt.grid()
plt.legend()

plt.savefig(
    "figures/microcavity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
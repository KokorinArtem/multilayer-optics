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

# Number of SiO2/TiO2 pairs
pairs = 10


def layer_angle(n0, theta0, n):
    """
    Calculate angle inside a layer using Snell's law.
    """
    return np.arcsin(n0 * np.sin(theta0) / n)


def layer_matrix(n, d, wavelength, theta, polarization):
    """
    Characteristic matrix of one optical layer.
    """

    delta = (
        2 * np.pi * n * d * np.cos(theta)
        / wavelength
    )

    if polarization == "s":
        eta = n * np.cos(theta)

    else:  # p-polarization
        eta = n / np.cos(theta)

    return np.array([
        [
            np.cos(delta),
            1j * np.sin(delta) / eta
        ],
        [
            1j * eta * np.sin(delta),
            np.cos(delta)
        ]
    ])


def reflectance_dbr(wavelength, theta0, polarization):
    """
    Reflectance of a DBR at a given wavelength,
    incidence angle and polarization.
    """

    theta_sio2 = layer_angle(
        n_air,
        theta0,
        n_sio2
    )

    theta_tio2 = layer_angle(
        n_air,
        theta0,
        n_tio2
    )

    theta_glass = layer_angle(
        n_air,
        theta0,
        n_glass
    )

    M = np.identity(2, dtype=complex)

    for _ in range(pairs):

        M_sio2 = layer_matrix(
            n_sio2,
            d_sio2,
            wavelength,
            theta_sio2,
            polarization
        )

        M_tio2 = layer_matrix(
            n_tio2,
            d_tio2,
            wavelength,
            theta_tio2,
            polarization
        )

        M = M @ M_sio2 @ M_tio2

    if polarization == "s":
        eta0 = n_air * np.cos(theta0)
        eta_sub = n_glass * np.cos(theta_glass)

    else:
        eta0 = n_air / np.cos(theta0)
        eta_sub = n_glass / np.cos(theta_glass)

    A = M[0, 0]
    B = M[0, 1]
    C = M[1, 0]
    D = M[1, 1]

    numerator = (
        eta0 * A
        + eta0 * eta_sub * B
        - C
        - eta_sub * D
    )

    denominator = (
        eta0 * A
        + eta0 * eta_sub * B
        + C
        + eta_sub * D
    )

    r = numerator / denominator

    return abs(r) ** 2


# Wavelength range
wavelengths = np.linspace(
    350e-9,
    800e-9,
    1000
)

# Incidence angles
angles_deg = [0, 15, 30, 45, 60]


# -------------------------
# s-polarization
# -------------------------

plt.figure(figsize=(10, 6))

for angle_deg in angles_deg:

    theta0 = np.radians(angle_deg)

    R = []

    for wavelength in wavelengths:
        R.append(
            reflectance_dbr(
                wavelength,
                theta0,
                "s"
            )
        )

    plt.plot(
        wavelengths * 1e9,
        R,
        label=f"{angle_deg}°"
    )

plt.axvline(
    lambda0 * 1e9,
    linestyle="--",
    label="550 nm"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance R")

plt.title(
    "DBR Angular Dependence — s-polarization"
)

plt.grid()
plt.legend()

plt.savefig(
    "figures/angular_dependence_s.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# -------------------------
# p-polarization
# -------------------------

plt.figure(figsize=(10, 6))

for angle_deg in angles_deg:

    theta0 = np.radians(angle_deg)

    R = []

    for wavelength in wavelengths:
        R.append(
            reflectance_dbr(
                wavelength,
                theta0,
                "p"
            )
        )

    plt.plot(
        wavelengths * 1e9,
        R,
        label=f"{angle_deg}°"
    )

plt.axvline(
    lambda0 * 1e9,
    linestyle="--",
    label="550 nm"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance R")

plt.title(
    "DBR Angular Dependence — p-polarization"
)

plt.grid()
plt.legend()

plt.savefig(
    "figures/angular_dependence_p.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
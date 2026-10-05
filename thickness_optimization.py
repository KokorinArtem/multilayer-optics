import numpy as np
import matplotlib.pyplot as plt

# Refractive indices
n_air = 1.0
n_sio2 = 1.46
n_tio2 = 2.40
n_glass = 1.50

# Target wavelength
lambda0 = 550e-9


def layer_matrix(n, d, wavelength):
    delta = 2 * np.pi * n * d / wavelength

    return np.array([
        [np.cos(delta), 1j * np.sin(delta) / n],
        [1j * n * np.sin(delta), np.cos(delta)]
    ])


def reflectance(d_sio2, d_tio2, wavelength):
    M1 = layer_matrix(n_sio2, d_sio2, wavelength)
    M2 = layer_matrix(n_tio2, d_tio2, wavelength)

    M = M1 @ M2

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


# Search range: 20–200 nm
sio2_values_nm = np.linspace(20, 200, 181)
tio2_values_nm = np.linspace(20, 200, 181)

R_map = np.zeros(
    (len(sio2_values_nm), len(tio2_values_nm))
)

best_R = 0
best_sio2 = 0
best_tio2 = 0

# Brute-force optimization
for i, d1_nm in enumerate(sio2_values_nm):

    for j, d2_nm in enumerate(tio2_values_nm):

        d1 = d1_nm * 1e-9
        d2 = d2_nm * 1e-9

        R = reflectance(d1, d2, lambda0)

        R_map[i, j] = R

        if R > best_R:
            best_R = R
            best_sio2 = d1_nm
            best_tio2 = d2_nm


# Theoretical quarter-wave thicknesses
quarter_sio2 = lambda0 / (4 * n_sio2) * 1e9
quarter_tio2 = lambda0 / (4 * n_tio2) * 1e9

print("Optimization results:")
print(f"Maximum reflectance: {best_R * 100:.2f}%")
print(f"Optimal SiO2 thickness: {best_sio2:.1f} nm")
print(f"Optimal TiO2 thickness: {best_tio2:.1f} nm")

print()
print("Quarter-wave thicknesses:")
print(f"SiO2: {quarter_sio2:.2f} nm")
print(f"TiO2: {quarter_tio2:.2f} nm")


# Heatmap
plt.figure(figsize=(10, 7))

plt.imshow(
    R_map.T,
    origin="lower",
    aspect="auto",
    extent=[
        sio2_values_nm[0],
        sio2_values_nm[-1],
        tio2_values_nm[0],
        tio2_values_nm[-1]
    ]
)

plt.colorbar(label="Reflectance R")

# Mark optimum
plt.scatter(
    best_sio2,
    best_tio2,
    marker="x",
    s=100,
    label="Maximum reflectance"
)

plt.xlabel("SiO2 thickness (nm)")
plt.ylabel("TiO2 thickness (nm)")

plt.title(
    "Optimization of Layer Thicknesses at 550 nm"
)

plt.legend()

plt.show()
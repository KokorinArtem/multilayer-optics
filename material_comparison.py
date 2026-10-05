import numpy as np
import matplotlib.pyplot as plt

# Refractive index of air
n1 = 1.0

# Materials and their approximate refractive indices
materials = {
    "Quartz": 1.46,
    "Glass": 1.50,
    "Sapphire": 1.77,
    "Diamond": 2.42
}

# Angles of incidence
theta1_deg = np.linspace(0, 89, 500)
theta1 = np.radians(theta1_deg)

# Create figure
plt.figure(figsize=(10, 6))

for material, n2 in materials.items():

    # Snell's law
    theta2 = np.arcsin((n1 / n2) * np.sin(theta1))

    # Fresnel equation for p-polarization
    Rp = (
        (n2 * np.cos(theta1) - n1 * np.cos(theta2))
        / (n2 * np.cos(theta1) + n1 * np.cos(theta2))
    ) ** 2

    # Brewster angle
    brewster_angle = np.degrees(np.arctan(n2 / n1))

    print(
        f"{material}: "
        f"n = {n2:.2f}, "
        f"Brewster angle = {brewster_angle:.2f} degrees"
    )

    # Plot reflectance
    plt.plot(
        theta1_deg,
        Rp,
        label=f"{material} (n={n2})"
    )

plt.xlabel("Angle of incidence (degrees)")
plt.ylabel("Reflectance Rp")
plt.title("Fresnel Reflection for Different Materials (p-polarization)")

plt.grid()
plt.legend()

plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Refractive indices
n1 = 1.0  # Air
n2 = 1.5  # Glass

# Angles of incidence from 0 to 89 degrees
theta1_deg = np.linspace(0, 89, 500)
theta1 = np.radians(theta1_deg)

# Snell's law
theta2 = np.arcsin((n1 / n2) * np.sin(theta1))

# Fresnel equations for s-polarization
Rs = (
    (n1 * np.cos(theta1) - n2 * np.cos(theta2))
    / (n1 * np.cos(theta1) + n2 * np.cos(theta2))
) ** 2

# Fresnel equations for p-polarization
Rp = (
    (n2 * np.cos(theta1) - n1 * np.cos(theta2))
    / (n2 * np.cos(theta1) + n1 * np.cos(theta2))
) ** 2

# Brewster angle
brewster_angle = np.degrees(np.arctan(n2 / n1))

print(f"Brewster angle: {brewster_angle:.2f} degrees")

# Plot
plt.figure(figsize=(9, 6))

plt.plot(theta1_deg, Rs, label="s-polarization")
plt.plot(theta1_deg, Rp, label="p-polarization")

plt.xlabel("Angle of incidence (degrees)")
plt.ylabel("Reflectance R")
plt.title("Fresnel Reflection: Air → Glass")

plt.grid()
plt.legend()
plt.savefig("figures/fresnel_reflection.png", dpi=300, bbox_inches="tight")
plt.show()
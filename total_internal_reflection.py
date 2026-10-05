import numpy as np
import matplotlib.pyplot as plt

# Light travels from glass to air
n1 = 1.5  # Glass
n2 = 1.0  # Air

# Critical angle
critical_angle = np.degrees(np.arcsin(n2 / n1))

print(f"Critical angle: {critical_angle:.2f} degrees")

# Angles of incidence
theta1_deg = np.linspace(0, 89, 1000)
theta1 = np.radians(theta1_deg)

# Arrays for reflectance
Rs = np.zeros_like(theta1)
Rp = np.zeros_like(theta1)

for i, angle in enumerate(theta1):

    sin_theta2 = (n1 / n2) * np.sin(angle)

    # Total internal reflection
    if sin_theta2 > 1:
        Rs[i] = 1.0
        Rp[i] = 1.0

    else:
        theta2 = np.arcsin(sin_theta2)

        # s-polarization
        Rs[i] = (
            (n1 * np.cos(angle) - n2 * np.cos(theta2))
            / (n1 * np.cos(angle) + n2 * np.cos(theta2))
        ) ** 2

        # p-polarization
        Rp[i] = (
            (n2 * np.cos(angle) - n1 * np.cos(theta2))
            / (n2 * np.cos(angle) + n1 * np.cos(theta2))
        ) ** 2

# Plot
plt.figure(figsize=(10, 6))

plt.plot(theta1_deg, Rs, label="s-polarization")
plt.plot(theta1_deg, Rp, label="p-polarization")

# Critical angle
plt.axvline(
    critical_angle,
    linestyle="--",
    label=f"Critical angle = {critical_angle:.2f}°"
)

plt.xlabel("Angle of incidence (degrees)")
plt.ylabel("Reflectance R")
plt.title("Total Internal Reflection: Glass → Air")

plt.grid()
plt.legend()

plt.show()
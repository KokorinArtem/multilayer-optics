# Computational Modeling of Optical Properties of Multilayer Materials

## Overview

This project investigates the optical properties of dielectric materials and multilayer structures using numerical modeling in Python.

The project focuses on Fresnel reflection, polarization, total internal reflection, thin-film interference, and optimization of multilayer optical structures.

The main goal is to study how refractive index, wavelength, layer order, number of layers, and layer thickness influence optical reflectance.

## Methods

The simulations are based on:

- Snell's law
- Fresnel equations
- Brewster angle
- Total internal reflection
- Transfer Matrix Method (TMM)
- Numerical parameter optimization

Python libraries used:

- NumPy
- Matplotlib

## Project Structure

### 1. Fresnel Reflection

Reflection of s- and p-polarized light at an air-glass interface was modeled using the Fresnel equations.

For glass with n = 1.50, the Brewster angle was approximately:

56.31 degrees.

### 2. Comparison of Optical Materials

The optical response of several materials was compared:

- Quartz
- Glass
- Sapphire
- Diamond

The simulations demonstrated that increasing the refractive index increases the Brewster angle and changes the angular dependence of reflectance.

### 3. Total Internal Reflection

Light propagation from glass to air was investigated.

The calculated critical angle was:

41.81 degrees.

Above this angle, the reflectance becomes R = 1, corresponding to total internal reflection.

### 4. Multilayer Optical Structure

A two-layer structure was modeled:

Air → SiO2 → TiO2 → Glass

The Transfer Matrix Method was used to calculate wavelength-dependent reflectance.

### 5. Influence of Layer Order and Number

Different multilayer configurations were compared.

Reflectance at 550 nm:

- Bare glass: 4.00%
- SiO2 / TiO2: 8.18%
- TiO2 / SiO2: 36.51%
- (SiO2 / TiO2) × 3: 73.74%

The results demonstrate the strong influence of layer order and the number of layers on optical reflectance.

### 6. Thickness Optimization

A numerical parameter search was performed to maximize reflectance at 550 nm.

For the SiO2 / TiO2 structure, the search produced:

- Maximum reflectance: 34.43%
- SiO2 thickness: 188 nm
- TiO2 thickness: 172 nm

The results were visualized using a two-dimensional reflectance map.

## Conclusions

The simulations demonstrate that the optical properties of multilayer materials can be controlled through material selection, layer order, layer thickness, and the number of layers.

Increasing the number of dielectric layers can strongly increase reflectance in a selected wavelength range.

Numerical modeling provides a useful method for designing and analyzing multilayer optical structures.

## Future Work

Possible extensions include:

- wavelength-dependent refractive indices
- absorption in materials
- optimization of multilayer structures
- oblique incidence
- comparison with experimental data
- design of dielectric mirrors and anti-reflection coatings
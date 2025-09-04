import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# SIMULATED MSD DATA
# -----------------------------
# Suppose you already have `msd_big` and `time`
time = np.arange(num_steps) * dt
simulated_msd = msd_big  # from your previous model

# -----------------------------
# MODEL FUNCTION
# -----------------------------
def msd_model(t, a):
    return 3 * a * t**2

# -----------------------------
# FIT PARAMETER a
# -----------------------------
popt, pcov = curve_fit(msd_model, time, simulated_msd)
a_fit = popt[0]
print(f"Fitted parameter a = {a_fit:.5f}")

# -----------------------------
# CALCULATE ERRORS
# -----------------------------
msd_pred = msd_model(time, a_fit)
error = simulated_msd - msd_pred            # absolute error

# -----------------------------
# CHI-SQUARED CALCULATION
# -----------------------------
# Assume uniform error sigma=1 (or any constant if unknown)
sigma = 1.0
chi_squared = np.sum((error / sigma)**2)
reduced_chi_squared = chi_squared / (len(time) - 1)  # degrees of freedom = N - 1
print(f"Chi-squared: {chi_squared:.3f}")
print(f"Reduced Chi-squared: {reduced_chi_squared:.3f}")

# -----------------------------
# PLOT ERRORS
# -----------------------------
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(time, error, 'r')
plt.xlabel('Time')
plt.ylabel('Absolute Error')
plt.title('Absolute Error: Simulated MSD - Model MSD')
plt.grid(True)

# -----------------------------
# PLOT COMPARISON
# -----------------------------
plt.subplot(1,2,2)
plt.plot(time, simulated_msd, 'r', label='Simulated MSD')
plt.plot(time, msd_model(time, a_fit), 'b--', label=f'Model MSD = 3*a*t^2 (a={a_fit:.4f})')
plt.xlabel('Time')
plt.ylabel(r'MSD $\langle r^2 \rangle$')
plt.title('Comparison of Simulated MSD with Analytical Model')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

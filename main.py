import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# =========================
# GLOBAL PARAMETERS
# =========================
V = 100              # reactor volume (L)
C0_nominal = 1.0     # mol/L

# Arrhenius constants
k0 = 1e3
E = 5000             # J/mol
R = 8.314

# Economics
price_nominal = 12
raw_cost = 4
op_cost = 40
energy_coeff = 0.05
T_ambient = 300

# Batch timings
t_fill = 5
t_empty = 5
t_reaction = 30

minutes_per_year = 365 * 24 * 60


# =========================
# RATE CONSTANT
# =========================
def rate_constant(T):
    return k0 * np.exp(-E / (R * T))


# =========================
# BATCH MODEL
# =========================
def batch_profit(T, n_sim=100):
    profits = []

    for _ in range(n_sim):
        C0 = np.random.normal(C0_nominal, 0.05)
        T_var = np.random.normal(T, 5)
        price = np.random.normal(price_nominal, 1)

        k = rate_constant(T_var)
        X = 1 - np.exp(-k * t_reaction)

        output = V * C0 * X
        cycle_time = t_fill + t_reaction + t_empty
        production_rate = output / cycle_time

        revenue = production_rate * price
        cost = production_rate * raw_cost + op_cost + energy_coeff * (T_var - T_ambient)

        profits.append((revenue - cost) * minutes_per_year)

    return np.mean(profits)


# =========================
# CSTR MODEL
# =========================
def cstr_profit(F, T, n_sim=100):
    profits = []

    for _ in range(n_sim):
        C0 = np.random.normal(C0_nominal, 0.05)
        T_var = np.random.normal(T, 5)
        price = np.random.normal(price_nominal, 1)

        k = rate_constant(T_var)
        tau = V / F
        X = (k * tau) / (1 + k * tau)

        production_rate = F * C0 * X

        revenue = production_rate * price
        cost = production_rate * raw_cost + op_cost + energy_coeff * (T_var - T_ambient)

        profits.append((revenue - cost) * minutes_per_year)

    return np.mean(profits)


# =========================
# OBJECTIVE FUNCTION
# =========================
def objective(vars):
    F, T = vars

    if F <= 0 or T < 300 or T > 800:
        return 1e9

    return -cstr_profit(F, T)


# =========================
# OPTIMIZATION
# =========================
print("Running optimization...")

result = minimize(objective, [5, 350], bounds=[(1, 50), (300, 800)])

F_opt, T_opt = result.x
max_profit = -result.fun

print("\n===== OPTIMAL CONDITIONS =====")
print(f"Optimal Flow Rate (CSTR): {F_opt:.2f} L/min")
print(f"Optimal Temperature: {T_opt:.2f} K")
print(f"Max Expected Profit: ${max_profit:.2f} / year")


# =========================
# BATCH COMPARISON
# =========================
batch_opt_profit = batch_profit(T_opt)

print("\n===== PROCESS COMPARISON =====")
print(f"Batch Profit at optimal T: ${batch_opt_profit:.2f} / year")
print(f"CSTR Profit at optimum:   ${max_profit:.2f} / year")

if max_profit > batch_opt_profit:
    print(">>> Recommended Process: CONTINUOUS (CSTR)")
else:
    print(">>> Recommended Process: BATCH")


# =========================
# RISK ANALYSIS
# =========================
def profit_distribution(F, T, n_samples=300):
    samples = []

    for _ in range(n_samples):
        samples.append(cstr_profit(F, T, n_sim=1))

    return samples


profits = profit_distribution(F_opt, T_opt)

plt.figure(figsize=(6,4))
plt.hist(profits, bins=30)
plt.title("Profit Distribution under Uncertainty")
plt.xlabel("Profit ($/year)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


# =========================
# SENSITIVITY ANALYSIS
# =========================
F_range = np.linspace(1, 30, 20)
profits_F = [cstr_profit(F, T_opt, n_sim=50) for F in F_range]

plt.figure(figsize=(6,4))
plt.plot(F_range, profits_F)
plt.axvline(F_opt, linestyle='--', label='Optimal F')
plt.xlabel("Flow Rate")
plt.ylabel("Profit")
plt.title("Sensitivity to Flow Rate")
plt.legend()
plt.tight_layout()
plt.show()
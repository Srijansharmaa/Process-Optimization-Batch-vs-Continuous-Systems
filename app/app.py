import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

st.title("Process Optimization: Batch vs Continuous")

k0 = st.slider("Pre-exponential factor (k0)", 100.0, 5000.0, 1000.0)
E = st.slider("Activation Energy (J/mol)", 1000.0, 10000.0, 5000.0)
price = st.slider("Product Price ($/mol)", 5.0, 20.0, 12.0)
raw_cost = st.slider("Raw Material Cost ($/mol)", 1.0, 10.0, 4.0)
op_cost = st.slider("Operating Cost ($/min)", 10.0, 100.0, 40.0)
energy_coeff = st.slider("Energy Cost Coefficient", 0.01, 0.2, 0.05)

V = 100
C0 = 1.0
R = 8.314
T_ambient = 300
minutes_per_year = 365 * 24 * 60


def rate_constant(T):
    return k0 * np.exp(-E / (R * T))


def simulate_profit(F, T, n_sim=50):
    profits = []

    for _ in range(n_sim):
        C0_var = np.random.normal(C0, 0.05)
        T_var = np.random.normal(T, 5)
        price_var = np.random.normal(price, 1)

        k = rate_constant(T_var)
        tau = V / F
        X = (k * tau) / (1 + k * tau)

        production = F * C0_var * X

        revenue = production * price_var
        cost = production * raw_cost + op_cost + energy_coeff*(T_var - T_ambient)

        profits.append((revenue - cost) * minutes_per_year)

    return np.mean(profits)


def objective(vars):
    F, T = vars

    if F <= 0 or T < 300 or T > 800:
        return 1e9

    return -simulate_profit(F, T)

if st.button("Run Optimization"):

    result = minimize(objective, [5, 350], bounds=[(1,50),(300,800)])
    F_opt, T_opt = result.x
    max_profit = -result.fun

    st.subheader("Optimal Conditions")
    st.write(f"Flow Rate: {F_opt:.2f} L/min")
    st.write(f"Temperature: {T_opt:.2f} K")
    st.write(f"Expected Profit: ${max_profit:.2f} / year")

   
    profits = [simulate_profit(F_opt, T_opt, n_sim=1) for _ in range(200)]

    fig, ax = plt.subplots()
    ax.hist(profits, bins=30)
    ax.set_title("Profit Distribution (Risk)")
    ax.set_xlabel("Profit")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)
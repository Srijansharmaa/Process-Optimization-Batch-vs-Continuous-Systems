# Process Optimization: Batch vs Continuous Systems

## Overview

This project started with a simple question:

When should we use a batch process, and when is continuous processing actually better?

To explore this, I built a simulation that compares both systems not just in terms of conversion, but based on real engineering trade-offs such as cost, efficiency, and uncertainty. The model goes beyond theory by incorporating economic analysis and optimization to identify the most profitable operating conditions.

---

## What This Project Does

- Simulates batch and continuous (CSTR) reactors  
- Uses temperature-dependent kinetics (Arrhenius equation)  
- Compares systems based on profit rather than just conversion  
- Accounts for real-world variability using Monte Carlo simulation  
- Optimizes operating conditions (flow rate and temperature)  
- Includes an interactive Streamlit application  

---

## Why This Matters

In real industrial settings, engineers do not only look at performance metrics like conversion. The actual question is:

Which setup is more profitable and reliable under changing conditions?

This project is designed to answer that by combining process modeling with economic and uncertainty analysis.

---

## Tech Stack

- Python  
- NumPy  
- SciPy  
- Matplotlib  
- Streamlit  

---

## Methodology

1. Modeled batch and continuous reactors using mass balance equations  
2. Incorporated temperature-dependent kinetics using the Arrhenius equation  
3. Developed an economic model including:
   - Product revenue  
   - Raw material cost  
   - Operating cost  
   - Energy cost  
4. Introduced uncertainty using Monte Carlo simulation:
   - Feed concentration variation  
   - Temperature fluctuation  
   - Market price variability  
5. Performed optimization to determine:
   - Optimal flow rate  
   - Optimal temperature  
   - Maximum expected profit  

---

## Key Insights

- Continuous processes generally perform better at scale due to steady operation  
- Higher temperature increases reaction rate but also increases energy cost  
- Ignoring uncertainty can lead to unrealistic or unstable decisions  
- Optimal performance comes from balancing kinetics, cost, and risk  

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
python main.py
streamlit run app.py

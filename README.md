# Simple GBM Stock Price Predictor (Daily)

This project implements a **Geometric Brownian Motion (GBM)** model to forecast future stock prices using historical **daily closing prices**.  
The model estimates drift and volatility from data, simulates future price paths using Monte Carlo methods, and reports the **median forecast** along with a **95% confidence interval**.

> **Disclaimer**  
> This project is for **educational purposes only** and is **not financial advice**.  
> GBM is a simplified model and does not account for dividends, jumps, regime changes, transaction costs, or macroeconomic effects.

---

## Files

- `stock_predictor.py` — Main Python script  
- `README.md` — Project documentation  

---

## Geometric Brownian Motion (GBM)

Geometric Brownian Motion is a continuous-time stochastic process commonly used to model stock prices.

The GBM stochastic differential equation (SDE) is:

dS_t = μ S_t dt + σ S_t dW_t

where:
- S_t — stock price at time t  
- μ — drift (expected return)  
- σ — volatility  
- W_t — standard Brownian motion  

---

## Closed-Form GBM Solution

Solving the SDE yields the analytical solution:

S_t = S_0 · exp((μ − 0.5 σ²)t + σ W_t)

This is the core equation used in the simulation.

---

## Parameter Estimation from Historical Data

Let P_0, P_1, ..., P_n denote daily closing prices.

### Log Returns

Daily log returns are computed as:

r_i = ln(P_i / P_{i−1})

---

### Volatility Estimation (σ)

Annualized volatility is estimated using the standard deviation of daily log returns:

σ = sqrt(252) · std(r)

where 252 is the approximate number of trading days per year.

---

### Drift Estimation (μ)

Annualized drift is estimated as:

μ = 252 · mean(r) + 0.5 σ²

The +0.5 σ² term converts the mean log return into arithmetic drift.

---

## Monte Carlo Simulation (Daily)

### Time Step

Δt = 1 / 252

---

### Brownian Motion Increments

ΔW_t ~ N(0, Δt)

Cumulative Brownian motion:

W_t = Σ ΔW_i

---

### Simulated Price Paths

For t future trading days:

S_t = S_0 · exp(((μ − 0.5 σ²) t) / 252 + σ W_t)

This formula is implemented directly in the code.

---

## Forecast Statistics

### Median Forecast

Median_t = median(S_t)

---

### 95% Confidence Interval

Lower_t = 2.5th percentile of S_t  
Upper_t = 97.5th percentile of S_t  

---

## Expected Annual Return

The expected continuously compounded annual growth rate is:

μ − 0.5 σ²

This value is printed in the program output.

---

## Data & Forecast Horizon

- Historical data used: **last 252 trading days (~1 year)**
- Default forecast horizon: **126 trading days (~6 months)**
- Forecast dates use **business days only**

---

## Output

### Plot
- Historical prices
- Median GBM forecast
- 95% confidence band

### Console Output
- Current price
- Estimated drift and volatility
- Median forecast price
- Expected percentage change
- 95% confidence interval

---

## How to Run

```bash
python stock_predictor.py

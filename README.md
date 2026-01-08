# Simple GBM Stock Price Predictor (Daily)

This project implements a **Geometric Brownian Motion (GBM)** model to forecast future stock prices using historical daily closing prices. The model estimates drift and volatility from data, simulates future price paths, and reports the **median forecast** along with a **95% confidence interval**.

> **Disclaimer**: This project is for educational purposes only and is **not financial advice**. GBM is a simplified model and does not capture dividends, jumps, regime changes, or macroeconomic effects.

---

## Files

- `stock_predictor.py` — Main Python script
- `README.md` — Project documentation

---

## Geometric Brownian Motion (GBM)

Geometric Brownian Motion is a continuous-time stochastic process widely used to model stock prices.

The GBM stochastic differential equation (SDE) is:

\[
\boxed{dS_t = \mu S_t \, dt + \sigma S_t \, dW_t}
\]

where:
- \( S_t \) = stock price at time \( t \)
- \( \mu \) = drift (expected return)
- \( \sigma \) = volatility
- \( W_t \) = standard Brownian motion

---

## Closed-Form GBM Solution

Solving the SDE yields the analytical solution:

\[
\boxed{S_t = S_0 \exp\left((\mu - \tfrac{1}{2}\sigma^2)t + \sigma W_t\right)}
\]

This is the **core equation** used in the simulation.

---

## Parameter Estimation from Historical Data

Let \( P_0, P_1, \dots, P_n \) be daily closing prices.

### Log Returns

Daily log returns are computed as:

\[
\boxed{r_i = \ln\left(\frac{P_i}{P_{i-1}}\right)}
\]

---

### Volatility Estimation (\( \sigma \))

Annualized volatility is estimated using the standard deviation of daily log returns:

\[
\boxed{\sigma = \sqrt{252} \cdot \mathrm{std}(r)}
\]

where 252 is the approximate number of trading days per year.

---

### Drift Estimation (\( \mu \))

Annualized drift is estimated as:

\[
\boxed{\mu = 252 \cdot \mathrm{mean}(r) + \tfrac{1}{2}\sigma^2}
\]

The \( +\tfrac{1}{2}\sigma^2 \) term converts the mean log return into arithmetic drift.

---

## Monte Carlo Simulation (Daily)

### Time Step

One trading day is modeled as:

\[
\boxed{\Delta t = \frac{1}{252}}
\]

---

### Brownian Motion Increments

For each simulation:

\[
\boxed{\Delta W_t \sim \mathcal{N}(0, \Delta t)}
\]

Cumulative Brownian motion:

\[
\boxed{W_t = \sum_{i=1}^{t} \Delta W_i}
\]

---

### Simulated Price Paths

For \( n \) future trading days:

\[
\boxed{
S_t = S_0 \exp\left(
\frac{(\mu - \tfrac{1}{2}\sigma^2)t}{252} + \sigma W_t
\right)
}
\]

This formula is implemented directly in the code.

---

## Forecast Statistics

After simulating many price paths:

### Median Forecast

\[
\boxed{\text{Median}_t = \mathrm{median}(S_t)}
\]

---

### 95% Confidence Interval

\[
\boxed{\text{Lower}_t = \text{Percentile}_{2.5}(S_t)}
\]

\[
\boxed{\text{Upper}_t = \text{Percentile}_{97.5}(S_t)}
\]

---

## Expected Annual Return

The expected continuously compounded annual growth rate is:

\[
\boxed{\mu - \tfrac{1}{2}\sigma^2}
\]

This value is printed in the program output.

---

## Data & Forecast Horizon

- Historical data used: **last 252 trading days (~1 year)**
- Default forecast length: **126 trading days (~6 months)**
- Forecast dates use **business days only**

---

## Output

The script produces:

- 📊 A plot showing:
  - Historical prices
  - Median GBM forecast
  - 95% confidence band

- Console output including:
  - Current price
  - Estimated drift and volatility
  - Median forecast price
  - Expected percentage change
  - Confidence interval

---

## How to Run

```bash
python simple_gbm_predictor_days.py

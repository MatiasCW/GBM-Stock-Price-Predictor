"""
Stock price prediction using Geometric Brownian Motion (GBM)
Forecasts median and 95% confidence interval for daily steps
"""
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def estimate_gbm_parameters(prices):
    """Estimate drift (μ) and volatility (σ) from historical prices"""
    log_returns = np.log(prices[1:] / prices[:-1])
    sigma = np.std(log_returns) * np.sqrt(252)  # annual volatility
    mu = np.mean(log_returns) * 252 + 0.5 * sigma**2  # annual drift
    return mu, sigma

def simulate_gbm_daily(S0, mu, sigma, n_days, n_sim=1000):
    """Simulate GBM paths daily"""
    dt = 1/252  # one trading day in years
    dW = np.random.normal(0, np.sqrt(dt), (n_days, n_sim))
    W = np.cumsum(dW, axis=0)
    t = np.arange(n_days)  # Days as integers
    S = S0 * np.exp((mu - 0.5*sigma**2)*t[:, None]/252 + sigma*W)
    return S, t

def predict_stock_daily(ticker, n_days=126, n_sim=1000):  # ~6 months
    """Predict stock daily for n_days using historical data"""
    # Fetch data - using 500 days to ensure we have enough trading days
    data = yf.Ticker(ticker).history(period="500d")
    
    if data.empty or len(data) < 60:
        print(f"   Error: Insufficient data for {ticker}")
        print(f"   Data points available: {len(data)} (need at least 60)")
        return
    
    # Take only the last 252 trading days (approximately 1 year)
    if len(data) > 252:
        data = data.iloc[-252:]
    
    prices = data['Close'].values
    S0 = float(prices[-1])
    mu, sigma = estimate_gbm_parameters(prices)
    
    # Historical dates
    hist_dates = data.index
    
    # Simulate GBM
    S, t = simulate_gbm_daily(S0, mu, sigma, n_days, n_sim=n_sim)
    
    # Median and 95% confidence interval
    median = np.median(S, axis=1)
    lower = np.percentile(S, 2.5, axis=1)
    upper = np.percentile(S, 97.5, axis=1)
    
    # Generate forecast dates (business days only)
    last_date = hist_dates[-1]
    forecast_dates = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=n_days)
    
    # Plot
    plt.figure(figsize=(12, 6))
    
    # Plot historical data
    plt.plot(hist_dates, prices, color='blue', linewidth=2, label=f'Historical ({len(prices)} trading days)')
    
    # Plot forecast
    plt.plot(forecast_dates, median, color='red', linestyle='--', linewidth=2, label='Median forecast')
    plt.fill_between(forecast_dates, lower, upper, color='orange', alpha=0.3, label='95% Confidence Interval')
    
    # Formatting
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.title(f'{ticker} Daily Price Forecast (GBM Model)', fontsize=14, fontweight='bold')
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.gcf().autofmt_xdate()
    
    plt.tight_layout()
    plt.show()
    
    # Print key predictions
    print(f"\n{'='*60}")
    print(f" {ticker} FORECAST RESULTS")
    print(f"{'='*60}")
    print(f"Current price:               ${S0:.2f}")
    print(f"Data used:                   Last {len(prices)} trading days")
    print(f"Estimated annual drift (μ):   {mu:.4f} ({mu*100:.2f}%)")
    print(f"Estimated volatility (σ):     {sigma:.4f} ({sigma*100:.2f}%)")
    print(f"\nForecast for {n_days} trading days (~{n_days/21:.1f} months):")
    print(f"  Median price:              ${median[-1]:.2f}")
    print(f"    Expected change:         {((median[-1]/S0)-1)*100:+.1f}%")
    print(f"  95% Confidence Interval:   ${lower[-1]:.2f} to ${upper[-1]:.2f}")
    print(f"    Range:                   {((lower[-1]/S0)-1)*100:+.1f}% to {((upper[-1]/S0)-1)*100:+.1f}%")
    print(f"\nExpected annual return (μ - 0.5σ²): {(mu-0.5*sigma**2)*100:.2f}%")
    print(f"{'='*60}")

if __name__ == "__main__":
    print("Stock Price Predictor")
    print("=" * 60)
    
    ticker = input("Enter stock ticker: ").upper().strip()
    if not ticker:
        ticker = "AAPL"  # Default
    
    n_days_input = input("Number of trading days to forecast: ").strip()
    n_days = int(n_days_input) if n_days_input.isdigit() else 126 # Default
    
    print(f"\n Fetching data and running simulation for {ticker}...")

    predict_stock_daily(ticker, n_days)

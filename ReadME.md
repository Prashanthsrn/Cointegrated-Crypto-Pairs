# Cointegrated Crypto Pairs Statistical Arbitrage

## Overview

This project implements a **Statistical Arbitrage (StatArb) strategy** on cryptocurrency pairs using **cointegration and mean reversion principles**.

Instead of predicting price direction, the strategy exploits **temporary deviations from long-term equilibrium** between two cointegrated assets.

- **Goal:** Identify profitable pairs of cryptocurrencies whose prices move together, and trade when their spread deviates from the equilibrium.  
- **Assets analyzed:** BTC, ETH, MATIC, AVAX, etc.  
- **Timeframe:** Rolling windows of historical data (daily frequency).

---

## Problem Statement

Many crypto pairs have a **stable long-term relationship** (e.g., BTC–ETH). Short-term deviations in their relative price can be exploited:

1. **Identify cointegrated pairs:** pairs whose spread is stationary over time.  
2. **Measure deviation:** calculate z-score of spread.  
3. **Trade mean reversion:** go long the laggard, short the leader when spread exceeds thresholds.  

> This strategy is **market-neutral**, focusing on **spread reversion** rather than absolute price movement.

---

## Quantitative Approach

### 1. Cointegration

We model the relationship as:

Y_t = alpha + beta * X_t + epsilon_t

markdown
Copy code

- `Y_t, X_t` = prices of the pair  
- `epsilon_t` = residual (spread)  
- Test if `epsilon_t` is stationary using the **ADF test**  
- Cointegration implies the spread will **mean-revert**

---

### 2. Spread and Z-score

spread_t = Y_t - (alpha + beta * X_t)
z_t = (spread_t - mean) / std

yaml
Copy code

- `mean, std` = mean and standard deviation of spread in the rolling window  
- Trading signals are generated when `|z_t| > 1.0` (entry) and `|z_t| < 0.1` (exit)

---

### 3. Trading Rules

| Z-score  | Position                             |
|----------|--------------------------------------|
| z > +1   | Short spread (short Y, long X)      |
| z < -1   | Long spread (long Y, short X)       |
| z ≈ 0    | Exit position                        |

---

### 4. Risk Metrics

- **Total PnL** = cumulative profit/loss  
- **Sharpe Ratio** = risk-adjusted return  
- **Max Drawdown** = largest peak-to-trough loss

### Streamlit Frontend

The Streamlit interface provides:
- Dropdowns to select Crypto A and Crypto B
- Adjustable rolling window size
- Date range selectors
- Buttons for:
  - Test Cointegration
  - Run Backtest

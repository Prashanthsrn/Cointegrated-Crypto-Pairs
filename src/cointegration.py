# src/cointegration.py
import pandas as pd
from itertools import combinations
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint

# Load data
data = pd.read_csv('data/crypto_prices.csv', index_col=0, parse_dates=True)
symbols = data.columns.tolist()

def test_cointegration(X, Y):
    """Return Engle-Granger p-value, ADF p-value, alpha, beta"""
    t_stat, p_value, _ = coint(Y, X)
    X_const = sm.add_constant(X)
    model = sm.OLS(Y, X_const).fit()
    alpha = model.params['const']
    beta = model.params[X.name]
    spread = Y - (alpha + beta * X)
    adf_p = adfuller(spread)[1]
    return p_value, adf_p, alpha, beta

# Rolling window parameters
window = 60  # 60 days
step = 1

cointegrated_windows = []

for start in range(0, len(data) - window + 1, step):
    end = start + window
    sub_data = data.iloc[start:end]
    
    for s1, s2 in combinations(symbols, 2):
        X = sub_data[s1]
        Y = sub_data[s2]
        coint_p, adf_p, alpha, beta = test_cointegration(X, Y)
        if coint_p < 0.05 and adf_p < 0.05:
            cointegrated_windows.append({
                'pair': (s1, s2),
                'start': sub_data.index[0],
                'end': sub_data.index[-1],
                'alpha': alpha,
                'beta': beta
            })

# Save results
if cointegrated_windows:
    df_windows = pd.DataFrame(cointegrated_windows)
    df_windows.to_csv('data/cointegrated_windows.csv', index=False)
    print("Cointegrated windows found")
    print(df_windows)
else:
    print("No cointegrated windows found")

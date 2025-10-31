import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


entry_z = 1.0
exit_z = 0.1


prices = pd.read_csv('data/crypto_prices.csv', index_col=0, parse_dates=True)
windows = pd.read_csv('data/cointegrated_windows.csv', parse_dates=['start', 'end'])

def plot_trades(sub_data, spread, zscore, entry_z=1.0, exit_z=0.1):
    position = 0
    entry_points = []
    exit_points = []

    for i in range(len(sub_data)):
        if zscore.iloc[i] > entry_z and position != -1:
            position = -1
            entry_points.append((sub_data.index[i], spread.iloc[i], 'short'))
        elif zscore.iloc[i] < -entry_z and position != 1:
            position = 1
            entry_points.append((sub_data.index[i], spread.iloc[i], 'long'))
        elif abs(zscore.iloc[i]) < exit_z and position != 0:
            position = 0
            exit_points.append((sub_data.index[i], spread.iloc[i]))

    plt.figure(figsize=(14,6))
    plt.plot(sub_data.index, spread, label='Spread', color='black')
    plt.plot(sub_data.index, zscore, label='Z-score', color='orange')

    for date, val, typ in entry_points:
        color = 'green' if typ=='long' else 'red'
        plt.scatter(date, val, color=color, marker='^', s=100, label=f'Entry {typ}')

    for date, val in exit_points:
        plt.scatter(date, val, color='blue', marker='v', s=100, label='Exit')

    plt.axhline(0, color='gray', linestyle='--')
    plt.axhline(entry_z, color='red', linestyle='--', alpha=0.5)
    plt.axhline(-entry_z, color='green', linestyle='--', alpha=0.5)
    plt.axhline(exit_z, color='blue', linestyle='--', alpha=0.5)

    plt.title('Spread & Z-score with Trade Signals')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend(loc='best')
    plt.show()


all_trades = []

for idx, row in windows.iterrows():
    # CLEAN PAIR PARSING
    pair_str = row['pair'].replace('(', '').replace(')', '').replace("'", "")
    s1, s2 = [x.strip() for x in pair_str.split(',')]
    
    alpha = row['alpha']
    beta = row['beta']
    
    try:
        sub_data = prices.loc[row['start']:row['end'], [s1, s2]]
    except KeyError:
        print(f"Skipping window: {s1}, {s2} not found in prices")
        continue

    spread = sub_data[s2] - (alpha + beta * sub_data[s1])
    zscore = (spread - spread.mean()) / spread.std()

    position = 0
    pnl = 0
    trade_log = []

    for i in range(len(sub_data)):
        if zscore.iloc[i] > entry_z and position != -1:
            position = -1
            entry_price = spread.iloc[i]
        elif zscore.iloc[i] < -entry_z and position != 1:
            position = 1
            entry_price = spread.iloc[i]
        elif abs(zscore.iloc[i]) < exit_z and position != 0:
            pnl += (spread.iloc[i] - entry_price) * position
            trade_log.append(pnl)
            position = 0

    if trade_log:
        all_trades.extend(trade_log)

    if idx < 3:  
        plot_trades(sub_data, spread, zscore, entry_z, exit_z)


if all_trades:
    all_trades = np.array(all_trades)
    total_pnl = all_trades.sum()
    sharpe = np.mean(all_trades)/np.std(all_trades)*np.sqrt(252)
    max_dd = np.max(np.maximum.accumulate(all_trades) - all_trades)

    print(f"Total PnL: {total_pnl:.2f}")
    print(f"Sharpe ratio: {sharpe:.2f}")
    print(f"Max drawdown: {max_dd:.2f}")
else:
    print("No trades executed")

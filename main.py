import ccxt
import pandas as pd
from ta.trend import EMAIndicator

top_36_coins = {
    'BTC': 'BTC/USDT', 'ETH': 'ETH/USDT', 'BNB': 'BNB/USDT', 'XRP': 'XRP/USDT',
    'ADA': 'ADA/USDT', 'DOGE': 'DOGE/USDT', 'SOL': 'SOL/USDT', 'MATIC': 'MATIC/USDT',
    'LTC': 'LTC/USDT', 'DOT': 'DOT/USDT', 'SHIB': 'SHIB/USDT', 'TRX': 'TRX/USDT',
    'AVAX': 'AVAX/USDT', 'LINK': 'LINK/USDT', 'ATOM': 'ATOM/USDT', 'XLM': 'XLM/USDT',
    'FIL': 'FIL/USDT', 'APT': 'APT/USDT', 'ARB': 'ARB/USDT', 'OP': 'OP/USDT',
    'NEAR': 'NEAR/USDT', 'QNT': 'QNT/USDT', 'VET': 'VET/USDT', 'APE': 'APE/USDT',
    'ALGO': 'ALGO/USDT', 'GRT': 'GRT/USDT', 'XMR': 'XMR/USDT', 'MKR': 'MKR/USDT',
    'PEPE': 'PEPE/USDT', 'SUI': 'SUI/USDT', 'RNDR': 'RNDR/USDT', 'RPL': 'RPL/USDT',
    'AAVE': 'AAVE/USDT', 'FTM': 'FTM/USDT', 'EGLD': 'EGLD/USDT', 'AUDIO': 'AUDIO/USDT'
}

exchange = ccxt.binance({
    'enableRateLimit': True
})

timeframe = '4h' 

coins_below_ema36 = []

for coin, symbol in top_36_coins.items():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)

    df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    if len(df) < 36:
        continue

    df['ema36'] = EMAIndicator(close=df['close'], window=36).ema_indicator()

    latest_close = df.iloc[-1]['close']
    latest_ema36 = df.iloc[-1]['ema36']

    if latest_close < latest_ema36:
        coins_below_ema36.append((coin, symbol, latest_close, latest_ema36))

if coins_below_ema36:
    print("Coins currently trading below their 4h EMA36:")
    for c in coins_below_ema36:
        coin, symbol, close_price, ema_price = c
        print(f"{coin} ({symbol}): Close={close_price}, EMA36={ema_price}")
else:
    print("No coins are currently trading below their 4h EMA36.")

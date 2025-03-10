import ccxt
import pandas as pd
import numpy as np

def fetch_ohlcv_data(exchange, symbol, timeframe='5m', limit=100):
    """
    ccxt를 이용해 OHLCV(시가,고가,저가,종가,거래량) 데이터를 가져와 DataFrame으로 반환
    """
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_moving_averages(df, short_window=5, long_window=20):
    """
    단기/장기 이동평균 컬럼을 DataFrame에 추가
    """
    df['ma_short'] = df['close'].rolling(window=short_window).mean()
    df['ma_long'] = df['close'].rolling(window=long_window).mean()
    return df

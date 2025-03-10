import ccxt
import os
import pandas as pd
from config import API_KEY, SECRET_KEY, DEFAULT_SYMBOL, DEFAULT_TIMEFRAME


def create_exchange():
    """
    ccxt의 binanceusdm 객체를 생성하여 반환합니다.
    Testnet 환경을 위해 모든 관련 URL과 옵션을 설정합니다.
    """
    exchange = ccxt.binanceusdm({
        'apiKey': API_KEY,
        'secret': SECRET_KEY,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
            'fetchCurrencies': False,  # load_markets() 시 fetch_currencies() 호출 방지
        },
        'urls': {
            'api': {
                'public':      'https://testnet.binancefuture.com/fapi/v1',
                'private':     'https://testnet.binancefuture.com/fapi/v1',
                'fapiPublic':  'https://testnet.binancefuture.com/fapi/v1',
                'fapiPrivate': 'https://testnet.binancefuture.com/fapi/v1',
                'sapi':        'https://testnet.binancefuture.com/sapi/v1',
            }
        }
    })
    return exchange

def fetch_ohlcv_data(exchange, symbol=None, timeframe=None, limit=100):
    if symbol is None:
        symbol = DEFAULT_SYMBOL
    if timeframe is None:
        timeframe = DEFAULT_TIMEFRAME
    
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
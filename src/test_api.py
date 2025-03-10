import ccxt
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '..', '.env')
load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

if __name__ == '__main__':
    # ccxt binanceusdm 객체 생성
    exchange = ccxt.binanceusdm({
        'apiKey': API_KEY,
        'secret': SECRET_KEY,
        'enableRateLimit': True,
        'urls': {
            'api': {
                'public':      'https://testnet.binancefuture.com/fapi/v1',
                'private':     'https://testnet.binancefuture.com/fapi/v1',
                'fapiPublic':  'https://testnet.binancefuture.com/fapi/v1',
                'fapiPrivate': 'https://testnet.binancefuture.com/fapi/v1',
                'sapi':        'https://testnet.binancefuture.com/sapi/v1',
            }
        },
        'options': {
            'defaultType': 'future',
            'fetchCurrencies': False,
        }
    })
    
    # 시세 조회 테스트
    try:
        ticker = exchange.fetch_ticker('BTC/USDT')
        print("Ticker:", ticker)
    except Exception as e:
        print("Error fetching ticker:", e)
    
    # 잔고 조회 테스트
    try:
        balance = exchange.fetch_balance()
        print("Balance:", balance)
    except Exception as e:
        print("Error fetching balance:", e)

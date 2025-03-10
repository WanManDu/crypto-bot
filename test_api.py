import requests, time, hmac, hashlib, os
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

# Binance Futures Testnet의 올바른 Base URL (v2 사용)
base_url = "https://testnet.binancefuture.com/fapi/v2"

def get_account_info():
    endpoint = "/account"  # v2 엔드포인트
    timestamp = int(time.time() * 1000)
    params = {
        "timestamp": timestamp,
        "recvWindow": 10000
    }
    query_string = urlencode(params)
    signature = hmac.new(SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

account_info = get_account_info()
print(account_info)
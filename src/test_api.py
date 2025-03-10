import logging
from data_collector import create_exchange
from logger import setup_logger

def main():
    logger = setup_logger()
    exchange = create_exchange()

    # 시세 조회 테스트
    try:
        ticker = exchange.fetch_ticker('BTC/USDT')
        logger.info(f"[test_api] Ticker: {ticker}")
    except Exception as e:
        logger.exception("[test_api] Error fetching ticker")

    # 잔고 조회 테스트
    try:
        balance = exchange.fetch_balance()
        logger.info(f"[test_api] Balance: {balance}")
    except Exception as e:
        logger.exception("[test_api] Error fetching balance")

if __name__ == '__main__':
    main()

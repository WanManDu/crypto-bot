import time
import logging
from data_collector import create_exchange, fetch_ohlcv_data
from strategy import generate_signal
from trading_engine import execute_order, check_position_and_close, current_position
from logger import setup_logger
from config import DEFAULT_SYMBOL, DEFAULT_TIMEFRAME

def main():
    logger = setup_logger()
    exchange = create_exchange()
    amount = 0.01

    while True:
        try:
            #OHLCV 데이터 수집
            df = fetch_ohlcv_data(exchange, DEFAULT_SYMBOL, DEFAULT_TIMEFRAME, limit=50)
            if len(df) == 0:
                logger.info("No OHLCV data fetched. Retrying in 60s...")
                time.sleep(60)
                continue

            #현재 시세
            last_price = df.iloc[-1]['close']

            #기존 포지션이 있다면 손절/익절 체크
            check_position_and_close(exchange, DEFAULT_SYMBOL, last_price, amount)

            #이동평균 교차 전략으로 신호 생성
            signal = generate_signal(df)
            logger.info(f"Signal: {signal}, last_price={last_price}")

            #현재 포지션이 없고, 매수/매도 신호가 나오면 주문 실행
            if current_position is None and signal in ['buy', 'sell']:
                execute_order(exchange, DEFAULT_SYMBOL, signal, amount, last_price)


        except Exception as e:
            logger.exception(f"Error in main loop: {e}")

        time.sleep(60) #1분마다 반복

if __name__ == '__main__':
    main()
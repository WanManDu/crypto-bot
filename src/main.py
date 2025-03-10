import time
import logging
from data_collector import create_exchange, fetch_ohlcv_data
from strategy import generate_signal
from trading_engine import execute_order, check_position_and_close, current_position, reset_position
from logger import setup_logger
from config import DEFAULT_SYMBOL, DEFAULT_TIMEFRAME

def main():
    logger = setup_logger()
    exchange = create_exchange()
    amount = 0.05

    while True:
        try:
            #OHLCV 데이터 수집
            df = fetch_ohlcv_data(exchange, DEFAULT_SYMBOL, DEFAULT_TIMEFRAME, limit=50)
            if len(df) == 0:
                logger.info("No OHLCV data fetched. Retrying in 60s...")
                time.sleep(60)
                continue

            current_candle_ts = df.iloc[-1]['timestamp']
            #현재 시세
            last_price = df.iloc[-1]['close']

            #기존 포지션이 있다면 손절/익절 체크
            check_position_and_close(exchange, DEFAULT_SYMBOL, last_price, amount)

            #새로운 캔들이 생성되었을 때만 신호 평가 (입장 신호)
            if last_candle_ts is None or current_candle_ts != last_candle_ts:
                signal = generate_signal(df)
                logger.info(f"New candle detected. Signal: {signal}, last_price={last_price}")
                last_candle_ts = current_candle_ts
                #만약 현재 포지션이 없으면 신규 주문 실행
                if current_position is None and signal in ['buy', 'sell']:
                    execute_order(exchange, DEFAULT_SYMBOL, signal, amount, last_price)
                #반대로, 현재 포지션이 있고 반대 신호가 발생하면 청산
                elif current_position is not None:
                    if (current_position == 'long' and signal == 'sell') or (current_position == 'short' and signal =='buy'):
                        logger.info("Opposite signal detected. Closing current position.")
                        reset_position()

            else:
                logger.info(f"Same candle. Evaluating exit conditions only. last_price={last_price}")

        except Exception as e:
            logger.exception(f"Error in main loop: {e}")

        time.sleep(60) #1분마다 반복

if __name__ == '__main__':
    main()
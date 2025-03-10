import ccxt
import time

POSITION_SIZE = 1

def execute_order(exchange, symbol, side, amount):
    """
    매수/매도 주문을 실행하는 함수 (시장가 주문 가정)
    side: 'buy' or 'sell'
    amount: 수량
    """
    order = None
    if side == 'buy':
        order = exchange.create_market_buy_order(symbol, amount)
    elif side == 'sell':
        order = exchange.create_market_sell_order(symbol, amount)
    return order

def run_trading_bot(exchange, symbol, strategy_func, logger):
    """
    간단한 봇 로직 (반복 루프):
      1) OHLCV 데이터 수집
      2) 지표 계산
      3) 전략 시그널 분석
      4) 주문 실행
      5) 일정 시간 대기
    """
    while True:
        # 1) 시세 데이터 수집 (간단히 20개 캔들만)
        from data_collector import fetch_ohlcv_data, calculate_moving_averages
        df = fetch_ohlcv_data(exchange, symbol, '5m', 20)
        df = calculate_moving_averages(df, 5, 20)
        
        # 2) 전략 시그널
        df = strategy_func(df)  # 예: moving_average_crossover_signal
        signal = df.iloc[-1]['signal']
        
        # 3) 주문 실행 로직 (예시)
        if signal == 'buy':
            logger.info("Signal: BUY -> Execute buy order")
            execute_order(exchange, symbol, 'buy', POSITION_SIZE)
        elif signal == 'sell':
            logger.info("Signal: SELL -> Execute sell order")
            execute_order(exchange, symbol, 'sell', POSITION_SIZE)
        else:
            logger.info("Signal: HOLD -> No action")
        
        time.sleep(60)  # 1분 대기

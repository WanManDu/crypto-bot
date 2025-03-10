import logging

#간단한 글로벌 상태
current_position = None
entry_price = None
stop_loss = None
take_profit = None

def execute_order(exchange, symbol, side, amount, last_price, sl_ratio=0.01, tp_ratio=0.015):
    """
    신규 포지션 오픈 함수
    - side: 'buy' or 'sell'
    - amount: 매매 수량
    - last_price: 최근 시세 (손절/익절 계산용)
    - sl_ratio, tp_ratio: 손절/익절 비율 (기본 1% 손절, 1.5% 익절)
    """

    global current_position, entry_price, stop_loss, take_profit

    if current_position is not None:
        logging.info("Position already open. Ignoring new signal.")
        return None
    
    order = None
    if side == 'buy':
        order = exchange.create_market_buy_order(symbol, amount)
        current_position = 'long'
        entry_price = last_price
        stop_loss = entry_price * (1 - sl_ratio)
        take_profit = entry_price * (1 + tp_ratio)
    elif side == 'sell':
        order = exchange.create_market_sell_order(symbol, amount)
        current_position = 'short'
        entry_price = last_price
        stop_loss = entry_price * (1 + sl_ratio)
        take_profit = entry_price * (1 - tp_ratio)
    else:
        logging.info("No valid side to execute order.")
        return None
    
    logging.info(f"[execute_order] side={side}, entry_price={entry_price}, stop_loss={stop_loss}, take_profit]{take_profit}")
    return order

def check_position_and_close(exchange, symbol, last_price, amount):
    """
    현재 포지션이 있을 경우, 손절/익절 가격에 도달했는지 확인 후 포지션 청산
    """

    global current_position, entry_price, stop_loss, take_profit

    if current_position is None:
        #포지션이 없으면 할 일 없음
        return None
    
    #Long 포지션일 경우
    if current_position == 'long':
        if last_price <= stop_loss:
            #손절
            order = exchange.create_market_sell_order(symbol, amount)
            logging.info(f"[check_position_and_close] Stop loss triggered. Closed LONG at price={last_price}")
            reset_position()
            return order
        elif last_price >= take_profit:
            #익절
            order = exchange.create_market_sell_order(symbol, amount)
            logging.info(f"[check_position_and_close] Take profit triggered. Close Long at price={last_price}")
            reset_position()
            return order
        
    #SHORT 포지션일 경우
    elif current_position == 'short':
        if last_price >= stop_loss:
            #손절
            order = exchange.create_market_buy_order(symbol, amount)
            logging.info(f"[check_position_and_close] Stop loss triggered. Close SHORT at price={last_price}")
            reset_position()
            return order
        elif last_price <= take_profit:
            #익절
            order = exchange.create_market_buy_order(symbol, amount)
            logging.info(f"[check_position_and_close] Take profit triggered. Closed SHORT at price={last_price}")
            return order
        
    return None

def reset_position():
    """
    포지션 상태를 초기화
    """
    global current_position, entry_price, stop_loss, take_profit
    current_position = None
    entry_price = None
    stop_loss = None
    take_profit = None
    
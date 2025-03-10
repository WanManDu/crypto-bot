import pandas as pd

def generate_signal(df, short_window = 5, long_window = 20):
    """
    이동평균 교차 기반의 간단한 전략 신호를 생성
    -short_window : 단기 이동평균 기간
    -long_window : 장기 이동평균 기간

    반환값 : 'buy', 'sell', 'hold'
    """

    #이동평균 컬럼 생성
    df['ma_short'] = df['close'].rolling(window = short_window).mean()
    df['ma_long'] = df['close'].rolling(window = long_window).mean()

    #충분한 데이터가 없으면 hold
    if len(df) < long_window:
        return 'hold'
    
    last_short = df.iloc[-1]['ma_short']
    last_long = df.iloc[-1]['ma_long']
    prev_short = df.iloc[-2]['ma_short']
    prev_long = df.iloc[-2]['ma_long']

    #단기 ma를 장기 ma가 상향 돌파하면 buy
    if prev_short <= prev_long and last_short > last_long:
        return 'buy'

    #장기 ma를 단기 ma가 하향 돌파하면 sell
    if prev_short > prev_long and last_short <= last_long:
        return 'sell'
    
    return 'hold'
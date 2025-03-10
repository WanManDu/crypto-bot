def moving_average_crossover_signal(df):
    """
    이동평균 교차 전략:
    단기 MA > 장기 MA -> 'buy'
    단기 MA < 장기 MA -> 'sell'
    나머지 -> 'hold'
    """
    df['signal'] = 'hold'
    df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 'buy'
    df.loc[df['ma_short'] < df['ma_long'], 'signal'] = 'sell'
    return df

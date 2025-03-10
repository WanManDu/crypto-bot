import os
import ccxt
import logging
from config import API_KEY, SECRET_KEY, DEFAULT_SYMBOL
from logger import setup_logger
from strategy import moving_average_crossover_signal
from trading_engine import run_trading_bot

def main():
    logger = setup_logger("trade.log")

    # ccxt 거래소 객체 생성
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
    
    logger.info("Starting trading bot...")
    run_trading_bot(exchange, DEFAULT_SYMBOL, moving_average_crossover_signal, logger)

if __name__ == '__main__':
    main()

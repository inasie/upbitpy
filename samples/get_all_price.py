# -*- coding: utf-8 -*-

from upbitpy import Upbitpy
import logging


def print_tickers(items):
    for it in items:
        if it['market'].startswith('KRW'):
            logging.info('{}: {} 원'.format(it['market'], it['trade_price']))
        elif it['market'].startswith('BTC'):
            logging.info('{}: {} btc'.format(it['market'], format(it['trade_price'], '.8f')))
        elif it['market'].startswith('ETH'):
            logging.info('{}: {} eth'.format(it['market'], format(it['trade_price'], '.8f')))
        elif it['market'].startswith('USDT'):
            logging.info('{}: {} usdt'.format(it['market'], format(it['trade_price'], '.3f')))


def main():
    upbit = Upbitpy()

    # 모든 market 얻어오기
    all_market = upbit.get_market_all()

    # market 분류
    market_table = {
        'BTC': [],
        'KRW': [],
        'ETH': [],
        'USDT': []
    }
    for m in all_market:
        for key in market_table.keys():
            if m['market'].startswith(key):
                market_table[key].append(m['market'])

    # 마켓 별 가격을 가져와 출력
    for key in market_table.keys():
        logging.info('{} 마켓:'.format(key))
        tickers = upbit.get_ticker(market_table[key])
        print_tickers(tickers)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

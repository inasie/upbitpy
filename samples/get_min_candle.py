# -*- coding: utf-8 -*-

from upbitpy import Upbitpy
import datetime
import logging
import time

INTERVAL_MIN = 1 # 간격 (1,3,5,10,15,30,60,240)

# System 시간 기준으로 Timer를 돌리기 위한 function
# min=1 이라면, 7시 12분 35초에 function이 호출되었다면 25초 sleep
# min=5 이라면, 7시 12분 35초에 function이 호출되었다면 2분 25초 sleep
def wait(min):
    now = datetime.datetime.now()
    remain_second = 60 - now.second
    remain_second += 60 * (min - (now.minute % min + 1))
    time.sleep(remain_second)


def main():
    upbit = Upbitpy()
    keys = ['opening_price', 'trade_price', 'high_price', 'low_price', 'timestamp']

    while True:
        coin = 'KRW-BTC'
        candle = upbit.get_minutes_candles(INTERVAL_MIN, 'KRW-BTC')[0]
        logging.info('[{}] {}'.format(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'), coin))
        for key in keys:
            logging.info('\t{}: {}'.format(key, candle[key]))
        wait(INTERVAL_MIN)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

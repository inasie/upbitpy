# -*- coding: utf-8 -*-

from upbitpy import Upbitpy
import datetime
import logging
import time

INTERVAL_MIN = 5 # 간격

def wait(min):
    now = datetime.datetime.now()
    remain_second = 60 - now.second
    remain_second += 60 * (min - (now.minute % min + 1))
    time.sleep(remain_second)


# candle 요청 회수 제한이 걸리면 1초 sleep
def check_remaining_candles_req(upbit):
    ret = upbit.get_remaining_req()
    if ret is None:
        return
    if 'candles' not in ret.keys():
        return
    if int(ret['candles']['sec']) == 0:
        logging.debug('>>> sleep 1 seconds')
        time.sleep(1)


def main():
    upbit = Upbitpy()

    # 모든 원화 market 얻어오기
    all_market = upbit.get_market_all()
    krw_markets = []
    for m in all_market:
        if m['market'].startswith('KRW'):
            krw_markets.append(m['market'])

    candles_7d = dict()
    # 7일간 거래량
    for m in krw_markets:
        candles_7d[m] = upbit.get_weeks_candles(m, count=1)[0]
        check_remaining_candles_req(upbit)

    while True:
        logging.info('평균 거래량 대비 {}분 거래량 비율========================'.format(INTERVAL_MIN))
        for m in krw_markets:
            vol = upbit.get_minutes_candles(1, m, count=1)[0]['candle_acc_trade_volume']
            vol_7d = candles_7d[m]['candle_acc_trade_volume']
            vol_7d_avg = (((vol_7d/7.0)/24.0)/60.0)*INTERVAL_MIN
            vol_ratio = format((vol/vol_7d_avg)*100.0, '.2f')
            logging.info('[{}] {}% (거래량:{}, 평균:{})'.format(
                m, vol_ratio, format(vol, '.2f'), format(vol_7d_avg, '.2f')))
            check_remaining_candles_req(upbit)
        wait(INTERVAL_MIN)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()

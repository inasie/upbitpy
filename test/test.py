# -*- coding: utf-8 -*-
from upbitpy import Upbitpy
import unittest
import logging


class UpbitpyTest(unittest.TestCase):

    def test_get_market_all(self):
        upbit = Upbitpy()
        ret = upbit.get_market_all()
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_minutes_candles(self):
        upbit = Upbitpy()
        ret = upbit.get_minutes_candles(60, 'KRW-BTC')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_days_candles(self):
        upbit = Upbitpy()
        ret = upbit.get_days_candles('KRW-ADA')
        self.assertIsNotNone(ret)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_weeks_candles(self):
        upbit = Upbitpy()
        ret = upbit.get_weeks_candles('KRW-ICX')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_months_candles(self):
        upbit = Upbitpy()
        ret = upbit.get_months_candles('BTC-ETH')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_trades_ticks(self):
        upbit = Upbitpy()
        ret = upbit.get_trades_ticks('KRW-ICX')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_ticker(self):
        upbit = Upbitpy()
        ret = upbit.get_ticker(['KRW-ICX', 'KRW-ADA'])
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())

    def test_get_orderbook(self):
        upbit = Upbitpy()
        ret = upbit.get_orderbook(['KRW-ICX', 'KRW-ADA'])
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        logging.info(upbit.get_remaining_req())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()

# -*- coding: utf-8 -*-

from upbitpy import Upbitpy
import unittest
import logging

class UpbitpyExchangeTest(unittest.TestCase):
    KEY = ''
    SECRET = ''

    TEST_MARKET = ''
    TEST_BID_PRICE = 0
    TEST_VOLUME = 0

    def test_get_get_accounts(self):
        upbit = Upbitpy(self.KEY, self.SECRET)
        ret = upbit.get_accounts()
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)


    def test_get_chance(self):
        upbit = Upbitpy(self.KEY, self.SECRET)
        ret = upbit.get_chance(self.TEST_MARKET)
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)


    def test_order(self):
        upbit = Upbitpy(self.KEY, self.SECRET)
        ret = upbit.order(self.TEST_MARKET, 'bid', self.TEST_VOLUME, self.TEST_BID_PRICE)
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        self.__do_cancel(upbit)


    def test_get_orders(self):
        upbit = Upbitpy(self.KEY, self.SECRET)
        self.__do_temp_order(upbit)
        ret = upbit.get_orders(self.TEST_MARKET, 'wait')
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)
        self.__do_cancel(upbit)


    def test_cancel_order(self):
        upbit = Upbitpy(self.KEY, self.SECRET)
        uuid = self.__do_temp_order(upbit)
        self.assertIsNotNone(uuid)
        ret = upbit.cancel_order(uuid)
        self.assertIsNotNone(ret)
        self.assertNotEqual(len(ret), 0)
        logging.info(ret)


    def __do_cancel(self, upbit):
        uuid = self.__get_temp_order(upbit)
        if uuid is not None:
            upbit.cancel_order(uuid)


    def __do_temp_order(self, upbit):
        upbit.order(self.TEST_MARKET, 'bid', self.TEST_VOLUME, self.TEST_BID_PRICE)
        ret = upbit.get_orders(self.TEST_MARKET, 'wait')
        if ret is None or len(ret) == 0:
            return None
        return ret[0]['uuid']


    def __get_temp_order(self, upbit):
        ret = upbit.get_orders(self.TEST_MARKET, 'wait')
        if ret is None or len(ret) == 0:
            return None
        return ret[0]['uuid']


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # key/secret 생성 방법:
    # 업비트 로그인 -> 마이페이지 -> Open API 관리 -> Open API Key 관리 -> 권한 설정 후 Open API Key 발급받기
    UpbitpyExchangeTest.KEY = 'put your key'
    UpbitpyExchangeTest.SECRET = 'put your secret'

    # 기본 테스트 환경: xrp, 10원에 100개 구매 (구매 요청 후 취소)
    UpbitpyExchangeTest.TEST_MARKET = 'KRW-XRP'
    UpbitpyExchangeTest.TEST_BID_PRICE = 10
    UpbitpyExchangeTest.TEST_VOLUME = 100

    unittest.main()

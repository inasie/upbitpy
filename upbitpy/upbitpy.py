# -*- coding: utf-8 -*-
import json
import time
import requests
import jwt
import logging
from urllib.parse import urlencode


class Upbitpy():
    """
    Upbit API
    https://docs.upbit.com/v1.0/reference
    """

    def __init__(self, access_key=None, secret=None):
        '''
        Constructor
        access_key, secret이 없으면 인증가능 요청(EXCHANGE API)은 사용할 수 없음
        :param str access_key: 발급 받은 acccess key
        :param str secret: 발급 받은 secret
        '''
        self.access_key = access_key
        self.secret = secret
        self.markets = self._load_markets()

    ###############################################################
    # EXCHANGE API
    ###############################################################

    def get_accounts(self):
        '''
        전체 계좌 조회
        내가 보유한 자산 리스트를 보여줍니다.
        https://docs.upbit.com/v1.0/reference#%EC%9E%90%EC%82%B0-%EC%A0%84%EC%B2%B4-%EC%A1%B0%ED%9A%8C
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/accounts'
        return self._get(URL, self._get_headers())

    def get_chance(self, market):
        '''
        주문 가능 정보
        마켓별 주문 가능 정보를 확인한다.
        https://docs.upbit.com/v1.0/reference#%EC%A3%BC%EB%AC%B8-%EA%B0%80%EB%8A%A5-%EC%A0%95%EB%B3%B4
        :param str market: Market ID
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/orders/chance'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        data = {'market': market}
        return self._get(URL, self._get_headers(data), data)

    def get_order(self, uuid):
        '''
        개별 주문 조회
        주문 UUID 를 통해 개별 주문건을 조회한다.
        https://docs.upbit.com/v1.0/reference#%EA%B0%9C%EB%B3%84-%EC%A3%BC%EB%AC%B8-%EC%A1%B0%ED%9A%8C
        :param str uuid: 주문 UUID
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/order'
        try:
            data = {'uuid': uuid}
            return self._get(URL, self._get_headers(data), data)
        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def get_orders(self, market, state, page=1, order_by='asc'):
        '''
        주문 리스트 조회
        주문 리스트를 조회한다.
        https://docs.upbit.com/v1.0/reference#%EC%A3%BC%EB%AC%B8-%EB%A6%AC%EC%8A%A4%ED%8A%B8-%EC%A1%B0%ED%9A%8C
        :param str market: Market ID
        :param str state: 주문 상태
            wait:체결 대기(default)
            done: 체결 완료
            cancel: 주문 취소
        :param int page: 페이지 수, default: 1
        :param str order_by: 정렬 방식
            asc: 오름차순(default)
            desc:내림차순
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/orders'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)

        if state not in ['wait', 'done', 'cancel']:
            logging.error('invalid state: %s' % state)
            raise Exception('invalid state: %s' % state)

        if order_by not in ['asc', 'desc']:
            logging.error('invalid order_by: %s' % order_by)
            raise Exception('invalid order_by: %s' % order_by)

        data = {
            'market': market,
            'state': state,
            'page': page,
            'order_by': order_by
        }
        return self._get(URL, self._get_headers(data), data)

    def order(self, market, side, volume, price):
        '''
        주문하기
        주문 요청을 한다.
        https://docs.upbit.com/v1.0/reference#%EC%A3%BC%EB%AC%B8%ED%95%98%EA%B8%B0-1
        :param str market: 마켓 ID (필수)
        :param str side: 주문 종류 (필수)
            bid : 매수
            ask : 매도
        :param str volume: 주문량 (필수)
        :param str price: 유닛당 주문 가격. (필수)
            ex) KRW-BTC 마켓에서 1BTC당 1,000 KRW로 거래할 경우, 값은 1000 이 된다.
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/orders'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)

        if side not in ['bid', 'ask']:
            logging.error('invalid side: %s' % side)
            raise Exception('invalid side: %s' % side)

        if market.startswith('KRW') and not self._is_valid_price(price):
            logging.error('invalid price: %.2f' % price)
            raise Exception('invalid price: %.2f' % price)

        data = {
            'market': market,
            'side': side,
            'volume': str(volume),
            'price': str(price),
            'ord_type': 'limit'
        }
        return self._post(URL, self._get_headers(data), data)

    def cancel_order(self, uuid):
        '''
        주문 취소
        주문 UUID를 통해 해당 주문을 취소한다.
        https://docs.upbit.com/v1.0/reference#%EC%A3%BC%EB%AC%B8-%EC%B7%A8%EC%86%8C
        :param str uuid: 주문 UUID
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/order'
        data = {'uuid': uuid}
        return self._delete(URL, self._get_headers(data), data)

    def get_withraws(self, currency, state, limit):
        '''
        출금 리스트 조회
        https://docs.upbit.com/v1.0/reference#%EC%A0%84%EC%B2%B4-%EC%B6%9C%EA%B8%88-%EC%A1%B0%ED%9A%8C
        :param str currency: Currency 코드
        :param str state: 출금 상태
            submitting : 처리 중
            submitted : 처리 완료
            almost_accepted : 출금대기중
            rejected : 거부
            accepted : 승인됨
            processing : 처리 중
            done : 완료
            canceled : 취소됨
        :param int limit: 갯수 제한
        :return: json array
        '''
        LIMIT_MAX = 100
        VALID_STATE = ['submitting', 'submitted', 'almost_accepted',
                       'rejected', 'accepted', 'processing', 'done', 'canceled']
        URL = 'https://api.upbit.com/v1/withdraws'
        data = {}
        if currency is not None:
            data['currency'] = currency
        if state is not None:
            if state not in VALID_STATE:
                logging.error('invalid state(%s)' % state)
                raise Exception('invalid state(%s)' % state)
            data['state'] = state
        if limit is not None:
            if limit <= 0 or limit > LIMIT_MAX:
                logging.error('invalid limit(%d)' % limit)
                raise Exception('invalid limit(%d)' % limit)
            data['limit'] = limit
        return self._get(URL, self._get_headers(data), data)

    def get_withraw(self, uuid):
        '''
        개별 출금 조회
        출금 UUID를 통해 개별 출금 정보를 조회한다.
        https://docs.upbit.com/v1.0/reference#%EA%B0%9C%EB%B3%84-%EC%B6%9C%EA%B8%88-%EC%A1%B0%ED%9A%8C
        :param str uuid: 출금 UUID
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/withdraw'
        data = {'uuid': uuid}
        return self._get(URL, self._get_headers(data), data)

    def get_withraws_chance(self, currency):
        '''
        출금 가능 정보
        해당 통화의 가능한 출금 정보를 확인한다.
        https://docs.upbit.com/v1.0/reference#%EC%B6%9C%EA%B8%88-%EA%B0%80%EB%8A%A5-%EC%A0%95%EB%B3%B4
        :param str currency: Currency symbol
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/withdraws/chance'
        data = {'currency': currency}
        return self._get(URL, self._get_headers(data), data)

    def withdraws_coin(self, currency, amount, address, secondary_address=None):
        '''
        코인 출금하기
        코인 출금을 요청한다.
        https://docs.upbit.com/v1.0/reference#%EC%BD%94%EC%9D%B8-%EC%B6%9C%EA%B8%88%ED%95%98%EA%B8%B0
        :param str currency: Currency symbol
        :param str amount: 출금 코인 수량
        :param str address: 출금 지갑 주소
        :param str secondary_address: 2차 출금 주소 (필요한 코인에 한해서)
        '''
        URL = 'https://api.upbit.com/v1/withdraws/coin'
        data = {
            'currency': currency,
            'amount': amount,
            'address': address
        }
        if secondary_address is not None:
            data['secondary_address'] = secondary_address
        return self._post(URL, self._get_headers(data), data)

    def withdraws_krw(self, amount):
        '''
        원화 출금하기
        원화 출금을 요청한다. 등록된 출금 계좌로 출금된다.
        https://docs.upbit.com/v1.0/reference#%EC%9B%90%ED%99%94-%EC%B6%9C%EA%B8%88%ED%95%98%EA%B8%B0
        :param str amount: 출금 원화 수량
        '''
        URL = 'https://api.upbit.com/v1/withdraws/krw'
        data = {'amount': amount}
        return self._post(URL, self._get_headers(data), data)

    def get_deposits(self, currency=None, limit=None, page=None, order_by=None):
        '''
        입금 리스트 조회
        https://docs.upbit.com/v1.0/reference#%EC%9E%85%EA%B8%88-%EB%A6%AC%EC%8A%A4%ED%8A%B8-%EC%A1%B0%ED%9A%8C
        :param str currency: Currency 코드
        :param int limit: 페이지당 개수
        :param int page: 페이지 번호
        :param str order_by: 정렬 방식
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/deposits'
        data = {}
        if currency is not None:
            data['currency'] = currency
        if limit is not None:
            data['limit'] = limit
        if page is not None:
            data['page'] = page
        if order_by is not None:
            data['order_by'] = order_by
        return self._get(URL, self._get_headers(data), data)

    def get_deposit(self, uuid):
        '''
        개별 입금 조회
        https://docs.upbit.com/v1.0/reference#%EA%B0%9C%EB%B3%84-%EC%9E%85%EA%B8%88-%EC%A1%B0%ED%9A%8C
        :param str uuid: 개별 입금의 UUID
        :return: json object
        '''
        URL = 'https://api.upbit.com/v1/deposit'
        data = {'uuid': uuid}
        return self._get(URL, self._get_headers(data), data)

    ###############################################################
    # QUOTATION API
    ###############################################################

    def get_market_all(self):
        '''
        마켓 코드 조회
        업비트에서 거래 가능한 마켓 목록
        https://docs.upbit.com/v1.0/reference#%EB%A7%88%EC%BC%93-%EC%BD%94%EB%93%9C-%EC%A1%B0%ED%9A%8C
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/market/all'
        return self._get(URL)

    def get_minutes_candles(self, unit, market, to=None, count=None):
        '''
        분(Minute) 캔들
        https://docs.upbit.com/v1.0/reference#%EB%B6%84minute-%EC%BA%94%EB%93%A4-1
        :param int unit: 분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240
        :param str market: 마켓 코드 (ex. KRW-BTC, BTC-BCC)
        :param str to: 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
        :param int count: 캔들 개수(최대 200개까지 요청 가능)
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/candles/minutes/%s' % str(unit)
        if unit not in [1, 3, 5, 10, 15, 30, 60, 240]:
            logging.error('invalid unit: %s' % str(unit))
            raise Exception('invalid unit: %s' % str(unit))
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)

        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)

    def get_days_candles(self, market, to=None, count=None):
        '''
        일(Day) 캔들
        https://docs.upbit.com/v1.0/reference#%EC%9D%BCday-%EC%BA%94%EB%93%A4-1
        :param str market: 마켓 코드 (ex. KRW-BTC, BTC-BCC)
        :param str to: 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
        :param int count: 캔들 개수
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/candles/days'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)

        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)

    def get_weeks_candles(self, market, to=None, count=None):
        '''
        주(Week) 캔들
        https://docs.upbit.com/v1.0/reference#%EC%A3%BCweek-%EC%BA%94%EB%93%A4-1
        :param str market: 마켓 코드 (ex. KRW-BTC, BTC-BCC)
        :param str to: 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
        :param int count: 캔들 개수
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/candles/weeks'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)

    def get_months_candles(self, market, to=None, count=None):
        '''
        월(Month) 캔들
        https://docs.upbit.com/v1.0/reference#%EC%9B%94month-%EC%BA%94%EB%93%A4-1
        :param str market: 마켓 코드 (ex. KRW-BTC, BTC-BCC)
        :param str to: 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
        :param int count: 캔들 개수
        :return: json array
        '''

        URL = 'https://api.upbit.com/v1/candles/months'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)

    def get_trades_ticks(self, market, to=None, count=None, cursor=None):
        '''
        당일 체결 내역
        https://docs.upbit.com/v1.0/reference#%EC%8B%9C%EC%84%B8-%EC%B2%B4%EA%B2%B0-%EC%A1%B0%ED%9A%8C
        :param str market: 마켓 코드 (ex. KRW-BTC, BTC-BCC)
        :param str to: 마지막 체결 시각. 형식 : [HHmmss 또는 HH:mm:ss]. 비워서 요청시 가장 최근 데이터
        :param int count: 체결 개수
        :param str cursor: 페이지네이션 커서 (sequentialId)
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/trades/ticks'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        if cursor is not None:
            params['cursor'] = cursor
        return self._get(URL, params=params)

    def get_ticker(self, markets):
        '''
        현재가 정보
        요청 당시 종목의 스냅샷을 반환한다.
        https://docs.upbit.com/v1.0/reference#%EC%8B%9C%EC%84%B8-ticker-%EC%A1%B0%ED%9A%8C
        :param str[] markets: 마켓 코드 리스트 (ex. KRW-BTC, BTC-BCC)
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/ticker'
        if not isinstance(markets, list):
            logging.error('invalid parameter: markets should be list')
            raise Exception('invalid parameter: markets should be list')

        if len(markets) == 0:
            logging.error('invalid parameter: no markets')
            raise Exception('invalid parameter: no markets')

        for market in markets:
            if market not in self.markets:
                logging.error('invalid market: %s' % market)
                raise Exception('invalid market: %s' % market)

        markets_data = markets[0]
        for market in markets[1:]:
            markets_data += ',%s' % market
        params = {'markets': markets_data}
        return self._get(URL, params=params)

    def get_orderbook(self, markets):
        '''
        호가 정보 조회
        https://docs.upbit.com/v1.0/reference#%ED%98%B8%EA%B0%80-%EC%A0%95%EB%B3%B4-%EC%A1%B0%ED%9A%8C
        :param str[] markets: 마켓 코드 목록 리스트 (ex. KRW-BTC,KRW-ADA)
        :return: json array
        '''
        URL = 'https://api.upbit.com/v1/orderbook?'
        if not isinstance(markets, list):
            logging.error('invalid parameter: markets should be list')
            raise Exception('invalid parameter: markets should be list')

        if len(markets) == 0:
            logging.error('invalid parameter: no markets')
            raise Exception('invalid parameter: no markets')

        for market in markets:
            if market not in self.markets:
                logging.error('invalid market: %s' % market)
                raise Exception('invalid market: %s' % market)

        markets_data = markets[0]
        for market in markets[1:]:
            markets_data += ',%s' % market
        params = {'markets': markets_data}
        return self._get(URL, params=params)

    ###############################################################

    def _get(self, url, headers=None, data=None, params=None):
        resp = requests.get(url, headers=headers, data=data, params=params)
        if resp.status_code not in [200, 201]:
            logging.error('get(%s) failed(%d)' % (url, resp.status_code))
            if resp.text is not None:
                logging.error('resp: %s' % resp.text)
                raise Exception('request.get() failed(%s)' % resp.text)
            raise Exception(
                'request.get() failed(status_code:%d)' % resp.status_code)
        return json.loads(resp.text)

    def _post(self, url, headers, data):
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code not in [200, 201]:
            logging.error('post(%s) failed(%d)' % (url, resp.status_code))
            if resp.text is not None:
                raise Exception('request.post() failed(%s)' % resp.text)
            raise Exception(
                'request.post() failed(status_code:%d)' % resp.status_code)
        return json.loads(resp.text)

    def _delete(self, url, headers, data):
        resp = requests.delete(url, headers=headers, data=data)
        if resp.status_code not in [200, 201]:
            logging.error('delete(%s) failed(%d)' % (url, resp.status_code))
            if resp.text is not None:
                raise Exception('request.delete() failed(%s)' % resp.text)
            raise Exception(
                'request.delete() failed(status_code:%d)' % resp.status_code)
        return json.loads(resp.text)

    def _load_markets(self):
        try:
            market_all = self.get_market_all()
            if market_all is None:
                return
            markets = []
            for market in market_all:
                markets.append(market['market'])
            return markets
        except Exception as e:
            logging.error(e)
            raise Exception(e)

    def _get_token(self, query):
        payload = {
            'access_key': self.access_key,
            'nonce': int(time.time() * 1000),
        }
        if query is not None:
            payload['query'] = urlencode(query)
        return jwt.encode(payload, self.secret, algorithm='HS256').decode('utf-8')

    def _get_headers(self, query=None):
        headers = {'Authorization': 'Bearer %s' % self._get_token(query)}
        return headers

    def _is_valid_price(self, price):
        '''
        원화 마켓 주문 가격 단위
        원화 마켓은 호가 별 주문 가격의 단위가 다릅니다. 아래 표를 참고하여 해당 단위로 주문하여 주세요.
        https://docs.upbit.com/v1.0/docs/%EC%9B%90%ED%99%94-%EB%A7%88%EC%BC%93-%EC%A3%BC%EB%AC%B8-%EA%B0%80%EA%B2%A9-%EB%8B%A8%EC%9C%84
        ~10         : 0.01
        ~100        : 0.1
        ~1,000      : 1
        ~10,000     : 5
        ~100,000    : 10
        ~500,000    : 50
        ~1,000,000  : 100
        ~2,000,000  : 500
        +2,000,000  : 1,000
        '''
        if price <= 10:
            if (price*100) != int(price*100):
                return False
        elif price <= 100:
            if (price*10) != int(price*10):
                return False
        elif price <= 1000:
            if price != int(price):
                return False
        elif price <= 10000:
            if (price % 5) != 0:
                return False
        elif price <= 100000:
            if (price % 10) != 0:
                return False
        elif price <= 500000:
            if (price % 50) != 0:
                return False
        elif price <= 1000000:
            if (price % 100) != 0:
                return False
        elif price <= 2000000:
            if (price % 500) != 0:
                return False
        elif (price % 1000) != 0:
            return False
        return True

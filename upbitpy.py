#-*- coding: utf-8 -*-
import json
import time
import requests
import jwt
import logging
from urllib.parse import urlencode


class Upbitpy():
  def __init__(self, access_key, secret):
    self.access_key = access_key
    self.secret = secret
    self.markets = self.get_markets()

  
  def get_markets(self):
    URL = "https://api.upbit.com/v1/market/all"
    try:
      resp = requests.get(URL)
      if resp.status_code != 200:
        logging.error('get_markets() failed(%d)' % resp.status_code)
        return None
      markets = []
      data_arr = json.loads(resp.text)
      for data in data_arr:
        markets.append(data['market'])
      return markets
    except Exception as e:
      logging.error(e)
      return None


  def get_token(self, query):
    payload = {
      'access_key': self.access_key,
      'nonce': int(time.time() * 1000),
    }
    if query is not None:
      payload['query'] = urlencode(query)
    return jwt.encode(payload, self.secret, algorithm='HS256').decode('utf-8')


  def get_headers(self, query=None):
    headers = {'Authorization': 'Bearer %s' % self.get_token(query) }
    return headers


  def get_ticker(self, markets):
    URL="https://api.upbit.com/v1/ticker?markets="
    try:
      if len(markets) == 0:
        logging.error('invalid parameter')
        return None
      for market in markets:
        if market not in self.markets:
          logging.error('invalid market: %s' % market)
          return None

      url = URL + markets[0]
      for market in markets[1:]:
        url += ',%s' % market

      resp = requests.get(url)
      if resp.status_code != 200:
        logging.error('get_ticker() failed(%d)' % resp.status_code)
        return None

      return json.loads(resp.text)

    except Exception as e:
      logging.error(e)
      return None


  def get_accounts(self):
    URL = "https://api.upbit.com/v1/accounts"
    try:
      resp = requests.get(URL, headers=self.get_headers())
      if resp.status_code != 200:
        logging.error('get_accounts() failed(%d)' % resp.status_code)
        return None
      json_data = json.loads(resp.text)
      return json_data
    except Exception as e:
      logging.error(e)
      return None


  def get_chance(self, market):
    URL = 'https://api.upbit.com/v1/orders/chance'
    try:
      if market not in self.markets:
        logging.error('invalid market: %s' % market)
        return None
      body = { 'market': market }
      resp = requests.get(URL, data=body, headers=self.get_headers(body))
      if resp.status_code != 200:
        logging.error('get_chance() failed(%d)' % resp.status_code)
        return None
      return json.loads(resp.text)
    except Exception as e:
      logging.error(e)
      return None


  def get_order(self, uuid):
    URL = "https://api.upbit.com/v1/order"
    try:
      body = { 'uuid': uuid }
      resp = requests.get(URL, data=body, headers=self.get_headers(body))
      if resp.status_code != 200:
        logging.error('get_order() failed(%d)' % resp.status_code)
        return None
      return json.loads(resp.text)
    except Exception as e:
      logging.error(e)
      return None


  # state: 'wait', 'done', 'cancel'
  # order_by: 'asc', 'desc'
  def get_orders(self, market, state, page=1, order_by='asc'):
    URL = "https://api.upbit.com/v1/orders"
    try:
      if market not in self.markets:
        logging.error('invalid market: %s' % market)
        return None
      
      if state not in ['wait', 'done', 'cancel']:
        logging.error('invalid state: %s' % state)
        return None
      
      if order_by not in ['asc', 'desc']:
        logging.error('invalid order_by: %s' % order_by)
        return None

      body = { 
        'market': market,
        'state': state,
        'page': page,
        'order_by': order_by
      }
      resp = requests.get(URL, data=body, headers=self.get_headers(body))
      if resp.status_code != 200:
        logging.error('get_order() failed(%d)' % resp.status_code)
        return None
      return json.loads(resp.text)
    except Exception as e:
      logging.error(e)
      return None


  # ~10         : 0.01
  # ~100        : 0.1
  # ~1,000      : 1
  # ~10,000     : 5
  # ~100,000    : 10
  # ~500,000    : 50
  # ~1,000,000  : 100
  # ~2,000,000  : 500
  # +2,000,000  : 1,000
  def is_valid_price(self, price):
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
    

  # side : 'bid'(buy), 'ask'(sell)
  def order(self, market, side, volume, price):
    URL = "https://api.upbit.com/v1/orders"
    try:
      if market not in self.markets:
        logging.error('invalid market: %s' % market)
        return None
      
      if side not in ['bid', 'ask']:
        logging.error('invalid side: %s' % side)
        return None

      if not self.is_valid_price(price):
        logging.error('invalid price: %.2f' % price)
        return None

      body = {
        'market': market,
        'side': side,
        'volume': str(volume),
        'price': str(price),
        'ord_type': 'limit'
      }
      resp = requests.post(URL, data=body, headers=self.get_headers(body))
      if resp.status_code != 201:
        logging.error('order failed(%d)' % resp.status_code)
        return None
      return json.loads(resp.text)
    except Exception as e:
      logging.error(e)
      return None

  
  def cancel_order(self, uuid):
    URL = 'https://api.upbit.com/v1/order'
    try:
      body = { 'uuid': uuid }
      resp = requests.delete(URL, data=body, headers=self.get_headers(body))
      if resp.status_code != 200:
        logging.error('cancel_order failed(%d)' % resp.status_code)
        return None
      return json.loads(resp.text)
    except Exception as e:
      logging.error(e)
      return None
  


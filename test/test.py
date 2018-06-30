# -*- coding: utf-8 -*-
from upbitpy import Upbitpy
from datetime import datetime
import logging


def print_json_data(data):
    if data is None:
        print('No data')
        return
    for key in data.keys():
        print('[%s] %s' % (key, data[key]))


def print_json_data_list(json_list):
    if json_list is None:
        print('No json_list')
        return
    for data in json_list:
        print('==============================')
        print_json_data(data)
    print('==============================')


logging.basicConfig(level=logging.DEBUG)
upbitpy = Upbitpy()
# upbitpy = Upbitpy('input access key', 'input secret')

###############################################################
# EXCHANGE API
###############################################################

# get accounts
# print_json_data_list(upbitpy.get_accounts())

# get chance
# print_json_data(upbitpy.get_chance('KRW-QTUM'))

# get order list
# print_json_data_list(upbitpy.get_orders('KRW-QTUM', 'done'))

# get order
# print_json_data(upbitpy.get_order('input uuid'))

# order
# print_json_data(upbitpy.order('KRW-QTUM', 'ask', 1, 15000))

# cancel order
# print_json_data(upbitpy.cancel_order('input uuid'))

# get withraws
# print_json_data_list(upbitpy.get_withraws('QTUM', 'done', 10))

# get withraw
# print_json_data(upbitpy.get_withraw('input uuid'))

# get withraws chance
# print_json_data(upbitpy.get_withraws_chance('QTUM'))

# withdraws coin (not tested)
# print_json_data(upbitpy.withdraws_coin('QTUM', 1, 'input address'))

# withdraws krw (not tested)
# print_json_data(upbitpy.withdraws_krw('1000000000'))

###############################################################
# QUOTATION API
###############################################################

# get market all
print_json_data_list(upbitpy.get_market_all())

# get candles - minutes
# print_json_data_list(upbitpy.get_minutes_candles(240, 'KRW-QTUM'))

# get candles - days
# print_json_data_list(upbitpy.get_days_candles('KRW-QTUM', count=10))

# get candles - weeks
# print_json_data_list(upbitpy.get_weeks_candles('KRW-EOS'))

# get candles - month
# print_json_data_list(upbitpy.get_months_candles('KRW-BTC'))

# get trades ticks
# print_json_data_list(upbitpy.get_trades_ticks('KRW-QTUM'))

# get ticker
# print_json_data_list(upbitpy.get_ticker(['KRW-BTC', 'BTC-ETH']))

# get orderbook
# print_json_data_list(upbitpy.get_orderbook(['KRW-QTUM', 'BTC-ETH']))

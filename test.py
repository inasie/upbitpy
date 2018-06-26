from upbitpy import Upbitpy

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
upbitpy = Upbitpy('your key', 'your secret')
#print_json_data_list(upbitpy.get_ticker(['KRW-BTC', 'BTC-ETH']))
#print_json_data_list(upbitpy.get_accounts())
#print_json_data(upbitpy.get_chance('KRW-QTUM'))
#print_json_data_list(upbitpy.get_orders('KRW-QTUM', 'done'))
#print_json_data(upbitpy.get_order('your uuid'))
#print_json_data(upbitpy.order('KRW-QTUM', 'ask', 1, 10000))
#print_json_data(upbitpy.cancel_order('your uuid'))
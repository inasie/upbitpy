# Upbitpy

[Upbit API](https://docs.upbit.com/v1.0/reference) for Python3

## Install dependency packages
```bash
$ pip install pyjwt
$ pip install requests
```

## Build/Install
```bash
$ python setup.py build
$ python setup.py install
```

## Usage
```python
from upbitpy import Upbitpy

upbit = Upbitpy()
tickers = upbit.get_ticker(['KRW-BTC', 'KRW-EOS'])
for ticker in tickers:
    print('%s trade price : %d' % (ticker['market'], ticker['trade_price']))
```

Please refer test/test.py for more samples

## Donate
|Cryptocurrency|Address|
|---|---|
|BTC|3LQ8rM139ehmGbqKwmKaEpiCyZhvGViLi8|
|BCH|34FczBgU3F4S9tympRncaZ9AAQTqkbFKDJ|
|ETH|0x3102857c163bc6ec97b358d877897a4bd9fcc556|
|QTUM|Qd9yEPh6KUcxTuz1k8MhWpmP44VnBkCsnD|
|ICON|hxdce20a7bf7437a0b5a062ea8d956a20460da7dc1|

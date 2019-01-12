# Upbitpy

[Upbit API](https://docs.upbit.com/v1.0/reference) for Python3

## Install
```bash
$ pip3 install upbitpy
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


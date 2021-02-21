import os
import sys
import json

from slovar import slovar
from slovar import split_strip

from signal import signal,SIGINT
from pprint import pprint as pp

from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

try:
    API_URL = os.environ['BINANCE_API_URL']
    API_KEY = os.environ['BINANCE_API_KEY']
    API_SECRET = os.environ['BINANCE_SECRET_KEY']
    TICKERS = split_strip(os.environ.get('TICKERS', ''))
    PRICE_ALERTS = split_strip(os.environ.get('PRICE_ALERTS', ''))
    DATA_PATH = os.environ['DATA_PATH']
except KeyError as er:
    print('Missing env var %s', er)
    sys.exit(1)

client = Client(API_KEY, API_SECRET)
client.API_URL = API_URL
bm = BinanceSocketManager(client)

def validate_tickers():
    print(f'Validating tickers {TICKERS}')
    valid_tickers = set([it['symbol']for it in client.get_all_tickers()])

    invalid_tickers = set(TICKERS) - valid_tickers
    if invalid_tickers:
        print(f'Invalid or unsupported ticker {invalid_tickers}')
        sys.exit(1)

def setup_ticker_files():
    print(f'Setting up files for {TICKERS}')
    ticker_files = {}

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    for each in TICKERS:
        _f  = open(os.path.join(DATA_PATH, f'{each}.json'), 'a+')
        ticker_files[each] = _f

    return ticker_files

def setup_price_alerts():
    price_alerts = {}
    for it in PRICE_ALERTS:
        _t,_p = it.split(':')
        price_alerts[_t] = float(_p)

    print(f'Setting up price alerts {price_alerts}')
    return price_alerts

def close_files(file_handles):
    for each in file_handles:
        each.close()

validate_tickers()
TICKER_FILES = setup_ticker_files()
PRICE_ALERT_MAP = setup_price_alerts()

def processor(msg):
    _d = slovar(msg).data.extract(
        [
        's__as__Symbol',
        'p__as__Price:float',
        ]
    )

    if _d.Symbol in PRICE_ALERT_MAP and _d.Price > PRICE_ALERT_MAP[_d.Symbol]:
        print(
            f'!!! Price alert !!! Ticker: {_d.Symbol}: Price:{_d.Price}, Alert Price: {PRICE_ALERT_MAP[_d.Symbol]}')

    TICKER_FILES[_d.Symbol].write(json.dumps(msg)+',\n')

def teardown(sig, frame):
    bm.close()
    reactor.stop()
    close_files(TICKER_FILES.values())
    print('EXIT!')

def main():
    print(f'Ingesting trade data for {TICKERS}')
    bm.start_multiplex_socket(
        ['%s@trade' % it.lower() for it in TICKERS],
        processor)

    bm.start()

if __name__ == '__main__':
    signal(SIGINT, teardown)
    main()

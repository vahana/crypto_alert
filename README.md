# crypto_alert

Dockerized python script to ingest binance trade data for specified tickers and print price alerts.

## Requirements
1. Docker
2. [python-binance](https://github.com/sammchardy/python-binance)
3. [slovar](https://github.com/vahana/slovar)

## Usage
```
git clone git@github.com:vahana/crypto_alert.git
cd crypto_alert
```

Open docker-compose.yml (or copy to docker-compose.override.yml) and adjust the environment variables to your needs.

example:
```
BINANCE_API_URL: https://testnet.binance.vision/api
BINANCE_API_KEY: "insert binance api key here"
BINANCE_SECRET_KEY: "insert binance secret key here"
TICKERS: BTCUSDT,ETHUSDT
PRICE_ALERTS: BTCUSDT:58999.50,ETHUSDT:2400.01
```

build and run with docker-compose
```
docker-compose build
docker-compose run coin_alert
```
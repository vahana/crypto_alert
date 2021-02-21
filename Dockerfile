FROM python:3.8

WORKDIR /coin_alert

RUN pip install python-binance
RUN pip install slovar

COPY main.py main.py

CMD ["python", "./main.py"]
import os, json
import tinvest as ti
from models import Stock


def get_market_stocks(client):
    payload = client.get_market_stocks().payload
    stocks_usd = [stock for stock in payload.instruments[:] if stock.currency == 'USD']
    stocks = {s.ticker: Stock(ticker=s.ticker, isin=s.isin) for s in stocks_usd}
    return stocks


def get_stocks():
    with open(os.path.join(os.path.expanduser('~'), 'no_commit', 'info.json')) as f:
        data = json.load(f)
    client = ti.SyncClient(data['token_tinkoff_real'])
    return get_market_stocks(client)

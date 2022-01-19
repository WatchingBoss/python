import os
import tinvest as ti
from openpyxl import Workbook
import concurrent.futures
from models import Portfolio
from market import get_client, show_get_portfolio, show_get_portfolio_currencies
from scrap import get_soup, get_finviz_table, check_hash, check_liquidity, get_avg_volume
import pandas as pd


def get_df(client, account) -> pd.DataFrame:
    currs = {
        ti.Currency.rub: 'RUB',
        ti.Currency.usd: 'USD'
    }
    types = {
        ti.InstrumentType.stock: 'Stock',
        ti.InstrumentType.bond: 'Bond'
    }
    title = ['Ticker', 'Name', 'Figi', 'Isin', 'Currency', 'Type', 'Balance', 'Price', 'Yield']
    df = pd.DataFrame(columns=title)
    for p in client.get_portfolio(account).payload.positions:
        if p.instrument_type not in types.keys():
            continue
        item = {
            'Ticker': p.ticker,
            'Name': p.name,
            'Figi': p.figi,
            'Isin': p.isin,
            'Currency': currs[p.average_position_price.currency],
            'Type': types[p.instrument_type],
            'Balance': int(p.balance),
            'Price': float(p.average_position_price.value),
            'Yield': float(p.expected_yield.value)
        }
        df = df.append(item, ignore_index=True)

    return df

def get_portfolios(client, acc_names) -> [Portfolio]:
    portfolios = list()
    for acc in acc_names.keys():
        portfolio = Portfolio(acc, acc_names[acc])
        portfolio.df = get_df(client, acc)
        portfolios.append(portfolio)
    return portfolios


def portfolio_to_table(path):
    client = get_client()
    # accounts = [a.broker_account_id for a in client.get_accounts().payload.accounts]
    acc_names = {
        '2011464472': 'Dividents',
        '2052923600': 'IIS'
    }
    portfolios = get_portfolios(client, acc_names)

    for p in portfolios:
        p.df['Sum'] = p.df.Price * p.df.Balance
        p.df.sort_values(by='Currency', inplace=True, ignore_index=True)

    for p in portfolios:
        print(p.df.to_string())

    with pd.ExcelWriter(path) as writer:
        for p in portfolios:
            p.df.to_excel(writer, sheet_name=p.name)


portfolio_to_table(os.path.join(os.path.curdir, 'portfolio.xlsx'))
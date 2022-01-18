import os
import tinvest as ti
from openpyxl import Workbook
import concurrent.futures
from models import Stock, Bond, Portfolio, Sheet
from market import get_client, show_get_portfolio, show_get_portfolio_currencies
from scrap import get_soup, get_finviz_table, check_hash, check_liquidity, get_avg_volume


def get_portfolio(client, account):
    stock_usd = list()
    stock_rub = list()
    bonds = list()
    for p in client.get_portfolio(account).payload.positions:
        item = object
        if p.instrument_type == ti.InstrumentType.stock:
            item = Stock(ticker=p.ticker, isin=p.isin)
        elif p.instrument_type == ti.InstrumentType.bond:
            item = Bond(ticker=p.ticker, isin=p.isin)
        else:
            continue
        item.ticker = p.ticker
        item.figi = p.figi
        item.currency = p.average_position_price.currency
        item.name = p.name
        item.type = p.instrument_type
        item.balance = int(p.balance)
        item.price = float(p.average_position_price.value)
        item.expected_yield = float(p.expected_yield.value)
        if item.type == 'Bond':
            item.currency = 'RUB'
            bonds.append(item)
        else:
            if item.currency == ti.Currency.rub:
                item.currency = 'RUB'
                stock_rub.append(item)
            elif item.currency == ti.Currency.usd:
                item.currency = 'USD'
                stock_usd.append(item)
    return stock_usd, stock_rub, bonds


def get_portfolios(client, acc_names) -> [Portfolio]:
    portfolios = list()
    for acc in acc_names.keys():
        portfolio = Portfolio(acc, acc_names[acc])
        usd, rub, bonds = get_portfolio(client, acc)
        portfolio.usd = usd
        portfolio.rub = rub
        portfolio.bond = bonds
        portfolios.append(portfolio)
    return portfolios


def fill_rows(item_list):
    if len(item_list) < 1:
        return list()
    rows = list()
    for i in range(len(item_list)):
        item = item_list[i]
        summery = item.price * item.balance
        change = item.expected_yield / summery
        rows.append([
            item.ticker,
            item.name,
            item.currency,
            item.price,
            item.balance,
            summery,
            item.expected_yield,
            change
        ])
    return rows


def portfolio_to_table(path):
    client = get_client()
    # accounts = [a.broker_account_id for a in client.get_accounts().payload.accounts]
    acc_names = {
        '2011464472': 'Dividents',
        '2052923600': 'IIS'
    }
    portfolios = get_portfolios(client, acc_names)
    sheets = list()
    title = ['Ticker', 'Name', 'Currency', 'Price', 'Balance', 'Sum', 'Yield', 'Change']
    sum_row = lambda stock_list: [
        '', '', '', '', '',
        sum([s.price * s.balance for s in p.rub]),
        sum([s.expected_yield for s in p.rub]),
        sum([s.expected_yield / (s.balance * s.price) for s in p.rub])
    ]
    for p in portfolios:
        sheet = Sheet(name=p.name, title=title)

        if p.rub is not None:
            for row in fill_rows(p.rub):
                sheet.rows.append(row)
            sheet.rows.append(sum_row(p.rub))

        if p.usd is not None:
            for row in fill_rows(p.usd):
                sheet.rows.append(row)
            sheet.rows.append(sum_row(p.usd))

        if p.bond is not None:
            for row in fill_rows(p.bond):
                sheet.rows.append(row)
            sheet.rows.append(sum_row(p.bond))

        sheets.append(sheet)

    wb = Workbook()
    ws = wb.active
    ws.title = portfolios[0].name

    for i in range(len(portfolios)):

        if i != 0:
            ws = wb.create_sheet(portfolios[i].name)

        for cal in range(len(title)):
            ws.cell(column=cal+1, row=1, value=title[cal])

        if sheets[i].rows is None:
            continue
        rows = sheets[i].rows

        for row in range(len(rows)):
            if rows[row] is None:
                continue
            for cal in range(len(rows[row])):
                ws.cell(column=cal + 1, row=row + 2, value=rows[row][cal])

    wb.save(path)


portfolio_to_table(os.path.join(os.path.curdir, 'portfolio.xlsx'))
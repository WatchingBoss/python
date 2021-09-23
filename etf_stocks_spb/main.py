from openpyxl import load_workbook, Workbook
import json
import os
import tinvest as tin
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import concurrent.futures


HEADER = {'User-Agent': str(UserAgent().chrome)}


class Stock:
    def __init__(self, ticker, isin):
        self.ticker = ticker
        self.isin = isin


class Sheet:
    def __init__(self, name):
        self.name = name
        self.title = ['Ticker', 'Weight', 'SPB', 'Short', 'ATR', 'Beta', 'Price', 'Avg volume']
        self.rows = []


def get_market_stocks(client, stocks_dict):
    payload = client.get_market_stocks().payload
    stocks_usd = [stock for stock in payload.instruments[:] if stock.currency == 'USD']
    for s in stocks_usd:
        stocks_dict[s.ticker] = Stock(s.ticker, s.isin)


def get_data(stocks_dict, f_path, sheets_list):
    wb = load_workbook(filename=f_path)
    for sheetname in wb.sheetnames:
        ws = wb[sheetname]
        sheet = Sheet(sheetname)

        for row in ws.rows:
            if row[0].value == "Ticker":
                continue
            spb = False
            if row[0].value in stocks_dict:
                spb = True
            sheet.rows.append([row[0].value, row[1].value, spb])

        sheets_list.append(sheet)


def show_sheets(sheets_list):
    for sheet in sheets_list:
        print(sheet.name)
        print(sheet.title)
        for row in sheet.rows:
            print(row)
        print('\n')


def add_short_info(sheets_list, stocks_dict):
    url = "https://www.tinkoff.ru/invest/margin/equities/"
    r = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(r.content, 'lxml')

    isin_able = {}

    all_tr = soup.find_all('tr', class_='Table__row_3Unlc Table__row_clickable_3EeUg')
    for tr in all_tr:
        all_td = tr.find_all('td')
        isin = all_td[1].text
        ability = all_td[2].text
        if ability == "Доступен":
            isin_able[isin] = True
        else:
            isin_able[isin] = False

    for sheet in sheets_list:
        for row in sheet.rows:
            if row[2]:
                try:
                    row.append(isin_able[stocks_dict[row[0]].isin])
                except KeyError:
                    row.append(False)


def check_hash(s):
    if s == '-':
        return 0
    return float(s)


def get_finviz_info(rows):
    for row in rows:
        if not row[2]:
            continue
        url = f"https://finviz.com/quote.ashx?t={row[0]}"
        r = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(r.content, 'lxml')

        table_mult = soup.find('table', class_='snapshot-table2')
        snapshot_td2_cp = table_mult.find_all('td', class_='snapshot-td2-cp')
        snapshot_td2 = table_mult.find_all('td', class_='snapshot-td2')
        mult = {snapshot_td2_cp[i].text.lower(): snapshot_td2[i].text.lower()
                for i in range(len(snapshot_td2))}

        row.append(check_hash(mult['atr']))
        row.append(check_hash(mult['beta']))
        row.append(check_hash(mult['price']))
        avg = mult['avg volume']
        if avg[-1] == 'm':
            avg = float(avg[0:-1]) * 1_000_000
        elif avg[-1] == 'k':
            avg = float(avg[0:-1]) * 1_000
        else:
            avg = float(avg[0:-1])
        row.append(avg)


def add_finviz_info(sheets_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for sheet in sheets_list:
            executor.submit(get_finviz_info, sheet.rows)
    # get_finviz_info(sheets_list[0].rows)


def write_sheet(sheets_list, f_path):
    wb = Workbook()
    ws = wb.active
    ws.title = sheets_list[0].name

    for i in range(len(sheets_list)):
        if i != 0:
            ws = wb.create_sheet(sheets_list[i].name)

        title = sheets_list[i].title
        rows = sheets_list[i].rows

        for cal in range(len(title)):
            ws.cell(column=cal+1, row=1, value=title[cal])

        for row in range(len(rows)):
            for cal in range(len(rows[row])):
                ws.cell(column=cal+1, row=row+2, value=rows[row][cal])

    wb.save(f_path)


def main():
    with open(os.path.join(os.path.expanduser('~'), 'no_commit', 'info.json')) as f:
        data = json.load(f)
        key = data['token_tinkoff_real']
    client = tin.SyncClient(key)

    all_stocks = {}
    my_sheets = []

    get_market_stocks(client, all_stocks)
    get_data(all_stocks, "etfs.xlsx", my_sheets)
    
    add_short_info(my_sheets, all_stocks)
    add_finviz_info(my_sheets)

    write_sheet(my_sheets, "etfs_holdings.xlsx")


if __name__ == '__main__':
    main()

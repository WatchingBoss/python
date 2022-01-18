from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import cloudscraper
from models import Liquidity

HEADER = {'User-Agent': str(UserAgent().chrome)}


def check_liquidity(stocks):
    url = "https://www.tinkoff.ru/invest/margin/equities/"
    r = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(r.content, 'lxml')

    liquidity = {}

    body_table = soup.find('table').find('tbody')
    trs = body_table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        isin = tds[1].text
        if tds[2].text == "Доступен":
            short_able = True
        else:
            short_able = False
        risk_long = float(tds[3].text.split('/')[0])
        risk_short = float(tds[3].text.split('/')[1])

        liquidity[isin] = Liquidity(short_able, risk_long, risk_short)

    for s in stocks:
        try:
            l = liquidity[s.isin]
            s.short = l.short_able
            s.risk = [l.risk_long, l.risk_short]
        except KeyError:
            continue


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


def get_avg_volume(avg):
    if avg[-1] == 'm':
        avg = float(avg[0:-1]) * 1_000_000
    elif avg[-1] == 'k':
        avg = float(avg[0:-1]) * 1_000
    else:
        avg = float(avg[0:-1])
    return avg


def check_hash(s):
    if s == '-':
        return 0
    return float(s)


def get_soup(url):
    scraper = cloudscraper.create_scraper()
    content = scraper.get(url).text
    return BeautifulSoup(content, 'lxml')


def get_finviz_table(soup: BeautifulSoup):
    table_mult = soup.find('table', class_='snapshot-table2')
    snapshot_td2_cp = table_mult.find_all('td', class_='snapshot-td2-cp')
    snapshot_td2 = table_mult.find_all('td', class_='snapshot-td2')
    mult = {snapshot_td2_cp[i].text.lower(): snapshot_td2[i].text.lower()
            for i in range(len(snapshot_td2))}
    return mult
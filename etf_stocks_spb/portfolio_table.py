from openpyxl import Workbook
import concurrent.futures
from models import Stock
from market import get_client, show_get_portfolio, show_get_portfolio_currencies
from scrap import get_soup, get_finviz_table, check_hash, check_liquidity, get_avg_volume


def portfolio_to_table():
    client = get_client()
    accounts = [a.broker_account_id for a in client.get_accounts().payload.accounts]
    for acc in client.get_accounts().payload.accounts:
        print(acc)
    # for acc in accounts:
    #     print(f"Account: {acc}")
    #     show_get_portfolio(client, acc)
    #     show_get_portfolio_currencies(client, acc)
    #     print('\n-----------------------------------\n-\n-\n-\n-\n----------------------------\n\n')


portfolio_to_table()
class Instrument:
    def __init__(self, ticker, isin=str()):
        self.ticker = ticker
        self.isin = isin


class Stock(Instrument):
    pass


class Bond(Instrument):
    pass


class Portfolio:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.rub = list()
        self.usd = list()
        self.bond = list()


# self.etf_title = ['Ticker', 'Weight', 'SPB', 'Short', 'ATR', 'Beta', 'Price', 'Avg volume']
# self.spb_title = ['Ticker', 'Name', 'Sector', 'Industry', 'Country']
# self.portfolio_title = ['Ticker', 'Name', 'Currency', 'Price', 'Balance', 'Sum', 'Yield', 'Change']


class Sheet:
    def __init__(self, name='default', title=None):
        self.name = name
        self.title = title
        self.rows = []


class Liquidity:
    def __init__(self, short_able, risk_long, risk_short):
        self.short_able = short_able
        self.risk_long = risk_long
        self.risk_short = risk_short

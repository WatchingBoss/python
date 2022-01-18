class Stock:
    def __init__(self, ticker, isin=str()):
        self.ticker = ticker
        self.isin = isin
        self.short = False
        self.risk = [float(), float()]
        self.atr = int()
        self.price = int()
        self.beta = int()
        self.atr_to_price = int()
        self.sector = str()
        self.industry = str()
        self.avg_volume = int()


class Sheet:
    def __init__(self, name='default'):
        self.name = name
        self.etf_title = ['Ticker', 'Weight', 'SPB', 'Short', 'ATR', 'Beta', 'Price', 'Avg volume']
        self.spb_title = ['Ticker', 'Name', 'Sector', 'Industry', 'Country']
        self.rows = []


class Liquidity:
    def __init__(self, short_able, risk_long, risk_short):
        self.short_able = short_able
        self.risk_long = risk_long
        self.risk_short = risk_short

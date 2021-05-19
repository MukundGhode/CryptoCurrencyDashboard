from cryptocmd import CmcScraper
from datetime import datetime
import time, logging, multiprocessing, locale
from flask import Flask, render_template
from numerize import numerize

tradable_coinswitch_kuber = {'DOGE': 'Dogecoin',
'LTC': 'Litecoin',
'NANO': 'Nano',
'BAND': 'Band-Protocol',
'DGB': 'DigiByte',
'XTZ': 'Tezos',
'ATOM': 'Cosmos',
'IOST': 'IOS Token',
'VET': 'VeChain',
'WAVES': 'Waves',
'THETA': 'Theta',
'ALGO': 'Algorand',
'TFUEL': 'Theta-Fuel',
'ZIL': 'Zilliqa',
'CHZ': 'Chiliz',
'DOT': 'Polkadot',
'EGLD': 'Elrond',
'LUNA': 'Terra',
'XEM': 'NEM',
'FIL': 'Filecoin',
'BTC': 'Bitcoin',
'ETH': 'Ethereum',
'XRP': 'Ripple',
'TRX': 'Tron',
'BNB': 'Binance-Coin',
'BCH': 'Bitcoin-Cash',
'ADA': 'Cardano',
'EOS': 'EOS',
'GAS': 'GAS',
'NEO': 'NEO',
'LINK': 'Chainlink',
'USDT': 'Tether',
'UNI': 'Uniswap',
'AAVE': 'Aave',
'DASH': 'Dash',
'TUSD': 'TrueUSD',
'USDC': 'USD-Coin',
'COMP': 'Compound',
'ZRX': '0x',
'ADX': 'AdEx',
'REP': 'Augur',
'BNT': 'Bancor',
'BAT': 'Basic-Attention-Token',
'CVC': 'Civic',
'ENJ': 'Enjin-Coin',
'FET': 'Fetch', #'Fetch.ai'
'GLM': 'Golem',
'BCHA': 'Bitcoin-Cash-ABC-2',
'KNC': 'Kyber-Network-Crystal-Legacy',
'MTL': 'Metal',
'OMG': 'OmiseGO',
'PAX': 'Paxos-Standard',
'POWR': 'Power-Ledger',
'DIA': 'DIA',
'QSP': 'Quantstamp',
'SUSHI': 'Sushi',
'NMR': 'Numeraire',
'YFI': 'Yearn-Finance',
'DAI': 'Multi-Collateral-Dai',
'LRC': 'Loopring',
'AST': 'AirSwap',
'REN': 'Ren',
'MKR': 'Maker',
'SXP': 'Swipe',
'QKC': 'QuarkChain',
'SNX': 'Synthetix-Network-Token',
'XLM': 'Stellar',
'YFII': 'Yearn-Finance-ii',
'RCN': 'Ripio-Credit-Network',
'SNT': 'Status',
'STORJ': 'Storj',
'ELF': 'aelf',
'DNT': 'district0x',
'MATIC': 'Polygon'
}

coinmarketcap_url = 'https://coinmarketcap.com/currencies/'
startThreadTime = time.time()
details = []

def get_details():
    locale.setlocale(locale.LC_ALL, '')
    for coin in tradable_coinswitch_kuber:
        try:
            # initialise scraper without time interval
            scraper = CmcScraper(coin)
            # scraper = CmcScraper("XRP", "15-10-2017", "25-10-2017")

            # get raw data as list of list
            # headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
            # headers, data = scraper.get_data()

            # Pandas dataFrame for the same data
            df = scraper.get_dataframe()

            # Percentage change = ((Today close - Yesterday Close)/ Yesterday Close)x100    format(percentage_change,".2f")
            percentage_change = format(((df['Close'][0] - df['Close'][1])/df['Close'][1])*100,".2f")# + " %"

            # percentage_change_last_7_days
            if len(df) > 7:
                percentage_change_last_7_days = format(((df['Close'][0] - df['Close'][7]) / df['Close'][7]) * 100,".2f")# + " %"
            else: percentage_change_last_7_days = 'NA'

            # percentage_change_this_month
            today = datetime.now().date() # datetime.date(2021, 5, 6)
            day = today.day
            if len(df) > day:
                # the dataframe has historical data. i.e. till yesterday, so day-1 for index starting from 0 and day-2 since data is 1 day previous
                percentage_change_this_month = format(((df['Close'][0] - df['Close'][day - 2]) / df['Close'][day - 2]) * 100,".2f")# + " %"
            else: percentage_change_this_month = 'NA'

            # percentage_change_this_year
            today = datetime.now().date()  # datetime.date(2021, 5, 6)
            new_year_day = datetime.now().date().replace(month=1, day=1)
            delta_days = today - new_year_day
            days = delta_days.days
            if len(df) > days:
                percentage_change_this_year = format(((df['Close'][0] - df['Close'][days]) / df['Close'][days]) * 100,".2f")# + " %"
            else: percentage_change_this_year = 'NA'

            # percentage_change_last90days
            if len(df) > 90:
                percentage_change_last90days = format(((df['Close'][0] - df['Close'][90]) / df['Close'][90]) * 100,".2f")# + " %"
            else:
                percentage_change_last90days = 'NA'

            # percentage_change_last180days
            if len(df) > 365:
                percentage_change_last180days = format(((df['Close'][0] - df['Close'][180]) / df['Close'][180]) * 100, ".2f")# + " %"
            else:
                percentage_change_last180days = 'NA'

            # percentage_change_last365days
            if len(df) > 365:
                percentage_change_last365days = format(((df['Close'][0] - df['Close'][365]) / df['Close'][365]) * 100,".2f")# + " %"
            else: percentage_change_last365days = 'NA'

            # percentage_change_all
            if len(df) >1:
                percentage_change_all = format(((df['Close'][0] - df['Close'][len(df)-1]) / df['Close'][len(df)-1]) * 100,".2f")# + " %"
            else: percentage_change_all = 'NA'

            # market cap
            if df['Market Cap'][0] > 0:
                # market_cap = "${}".format(numerize.numerize(df['Market Cap'][0],2))
                market_cap = df['Market Cap'][0]
            else: market_cap = 'NA'

            chart_url = "{}{}".format(coinmarketcap_url, tradable_coinswitch_kuber[coin].lower())

            detail = {
                'coin': coin,
                'Cryptoname': tradable_coinswitch_kuber[coin],
                'market_cap': market_cap,
                'open': "${}".format(locale.currency(float(format(df['Open'][0],".2f")), symbol=False, grouping=True)),
                'close': "${}".format(locale.currency(float(format(df['Close'][0],".2f")), symbol=False, grouping=True)),
                'high': "${}".format(locale.currency(float(format(df['High'][0],".2f")), symbol=False, grouping=True)),
                'low': "${}".format(locale.currency(float(format(df['Low'][0],".2f")), symbol=False, grouping=True)),
                'percentage_change': percentage_change,
                'percentage_change_last_7_days': percentage_change_last_7_days,
                'percentage_change_this_month': percentage_change_this_month,
                'percentage_change_this_year': percentage_change_this_year,
                'percentage_change_last90days': percentage_change_last90days,
                'percentage_change_last180days': percentage_change_last180days,
                'percentage_change_last365days': percentage_change_last365days,
                'percentage_change_all': percentage_change_all,
                'last_modified_date': df['Date'][0].date(),
                'chart_url':chart_url
            }
            details.append(detail)
            print("[OK] : Fetched data for {} - {}".format(coin, tradable_coinswitch_kuber[coin]))
            # if len(details) > 5: break
        except Exception  as e:
            print(repr(e))
            logging.error(logging.traceback.format_exc())
            logging.error("[KO] : Can't Fetch data for {} - {}".format(coin, tradable_coinswitch_kuber[coin]))
    return details


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('details.html', details=details)

if __name__ == '__main__':
    details = get_details()
    app.run()
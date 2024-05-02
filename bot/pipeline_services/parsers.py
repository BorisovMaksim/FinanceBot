import os
from tinkoff.invest import Client
from tinkoff.invest.schemas import InstrumentType
import yahooquery as yq
import numpy as np

from dotenv import load_dotenv
load_dotenv()




TOKEN = os.environ['TINKOFF_TOKEN']



def get_last_price_yahoo(query):
    try:
        data = yq.search(query)
    except ValueError: 
        print(query)
    else:
        quotes = data['quotes']
        if len(quotes) == 0:
            return 'No Symbol Found'

        symbol = quotes[0]['symbol']
        exchange = quotes[0]['exchDisp']
        ticker = yq.Ticker(symbol)
        price = ticker.summary_detail[symbol]['bid']
        return price, exchange
    
    
def get_all_companies_names():
    with Client(TOKEN) as client:   
        shares = client.instruments.shares()
    names = list({x.name for x in shares.instruments})
    return names
    
def get_last_price_tinkoff(query):
    with Client(TOKEN) as client:   
        shares = client.instruments.find_instrument(query=query, instrument_kind=InstrumentType.INSTRUMENT_TYPE_SHARE).instruments
        for share in shares:
            last_prices = client.market_data.get_last_prices(figi=[share.figi]).last_prices[0]
            if last_prices.price.units != 0:
                price = float(f"{last_prices.price.units}.{last_prices.price.nano}")
                return price
                            
                
if __name__ == '__main__':
    query = "Яндекс"
    price = get_last_price_tinkoff(query)
    print(query, price)
    
    query = "google"
    price, exchange = get_last_price_yahoo(query)
    print(query, price, exchange)
    
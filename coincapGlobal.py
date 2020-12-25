from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a0b47712-6af4-494c-88f6-b47417d2d024',
}


session = Session()
session.headers.update(headers)

try:
  response = session.get(url)
  ##deserializes json 
 
  results = response.json()
  print(json.dumps(results, sort_keys=True, indent=4))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


def formatTheStrings(theStrings):
    val = '{:,}'.format(theStrings)
    return val




active_currencies = results['data']['active_cryptocurrencies']
total_cyrprocurrencies = results['data']['total_cryptocurrencies']
active_marketPairs = results['data']['active_market_pairs']
btc_dominance = results['data']['btc_dominance']
altcoin_market_cap = results['data']['quote']['USD']['altcoin_market_cap']
altcoin_volume_24h = results['data']['quote']['USD']['altcoin_volume_24h']
last_updated = results['data']['last_updated']



##careful: cannot combine string and int tgt
print("There are currently " + formatTheStrings(active_currencies) + "active currencies and a total of " + formatTheStrings(total_cyrprocurrencies)+ " currencies")
print("There are currently "+ formatTheStrings(active_marketPairs) + " active markets")
print("The bit coin dominance percentage in the market is " + formatTheStrings(btc_dominance))
print("The bitcoin market cap is "+ formatTheStrings(altcoin_market_cap) + " and the bitcoin volume in the last 24 hours is " + formatTheStrings(altcoin_volume_24h))
print("The information was last updated on " + last_updated)
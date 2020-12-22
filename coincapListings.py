from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'f4c8add2-5d5a-4dc8-a1bc-295de4f75851',
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




storeTheBTC =[]
data = results['data']
for eachCurrency in data:
    currencyID = eachCurrency['id']
    currencyName = eachCurrency['name']
    currencySymbol = eachCurrency['symbol']
    bitInfo= (str(currencyID)+  ":" + currencyName + "("+ currencySymbol+ ")")
    print(bitInfo)
    storeTheBTC.append(bitInfo)


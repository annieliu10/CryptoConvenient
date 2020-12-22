import requests
import json

url = 'https://min-api.cryptocompare.com/data/pricemultifull'


flag= True
accum = 0
while flag:
    cryptoSymbol = input("What cryptocurrency are you looking for? ")
    if cryptoSymbol==" ":
        flag = False
    else: 
        if(accum >=1):
           url+=","+ cryptoSymbol
        else:
            url += "?fsyms=" + cryptoSymbol
    accum+= 1

anotherFlag= True
anotherAccum = 0
while anotherFlag:
    currency= input("What currency do you want it to be in?")
    if currency==" ":
        anotherFlag = False
    else: 
        if(anotherAccum >=1):
           url+=","+ currency
        else:
            url += "&tsyms=" + currency
    anotherAccum+= 1

response = requests.get(url)

data= response.json()

print(json.dumps(data, sort_keys=True, indent=4))




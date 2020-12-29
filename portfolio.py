import os
import json
import requests 
import re 
from datetime import datetime 
from prettytable import PrettyTable
from colorama import Fore, Back, Style
import time  


url = "https://min-api.cryptocompare.com/data/top/totalvolfull"

limit = input("How many coins do you want to request? Press return if you don't have a limit: ")



currency = 'USD'

if limit != "":
    url += '?limit='+ str(limit)
 
url += '&tsym=' + currency

response = requests.get(url)
response =response.json()


data = response['Data']
storeTopNames= []
for currency in data:
    symbol = currency['CoinInfo']['Name']
    storeTopNames.append(symbol)

print()
print("Here are the names of the top bitcoins you should choose from: ")
print(storeTopNames)    

file = open("portfolio.txt", "a")
alert_file = open ("alerts.txt", "a")

flag= True
while flag:
    coin_name= input("Enter coin name or press space return to quit: ")
    if (coin_name != ""):
        amounts = input("Enter amount you own: ")
        alerts = input("Enter the amount you want it to hit: ")
        file.write(coin_name + " " + amounts)
        file.write("\n")
        alert_file.write(coin_name + " " + alerts)
        alert_file.write("\n")
    else:
        flag = False
file.close()
alert_file.close()




portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Coin Asset', "Amount owned", "USD Value", 'Price', '1h', '24h', 'Market Cap'])

## text file for user to input in the coin name and the amount they want to invest in 

with open("portfolio.txt")as input:
    for line in input:
        tickerSymbol, amount = line.split()
        tickerSymbol = tickerSymbol.upper()
        storeTopNames.append(tickerSymbol)

        tickerURL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD'.format(tickerSymbol)

        result = requests.get(tickerURL)
        result = result.json()

        name = tickerSymbol
        price = result['RAW'][tickerSymbol]['USD']['PRICE']
        last_updated = result['RAW'][tickerSymbol]['USD']['LASTUPDATE']
        hour_change = result['RAW'][tickerSymbol]['USD']['CHANGEHOUR']
        day_change = result['RAW'][tickerSymbol]['USD']['CHANGE24HOUR']
        market_cap = result['DISPLAY'][tickerSymbol]['USD']['MKTCAP']
        
      
        valueOwned = float(amount)* float(price)
        portfolio_value += valueOwned
        
        valueFormatted ='{:,}'.format(round(valueOwned,2))
        priceFormatted ='{:,}'.format(round(price, 2))
        hourChangeFormatted= '{:,}'.format(round(hour_change, 2))
        dayChangeFormatted = '{:,}'.format(round(day_change, 2))

        if hour_change >0:
            hourChangeFormatted= Back.GREEN + hourChangeFormatted + "%" + Style.RESET_ALL
        else:
            hourChangeFormatted= Back.RED + hourChangeFormatted + "%" + Style.RESET_ALL

        if day_change >0:
            dayChangeFormatted= Back.GREEN + dayChangeFormatted + "%" + Style.RESET_ALL
        else:
            dayChangeFormatted= Back.RED + dayChangeFormatted + "%" + Style.RESET_ALL

        table.add_row([name,
        ##str(storeTopNames.index(tickerSymbol)+1),
        amount,
        valueFormatted,
        str(priceFormatted),
        str(hourChangeFormatted),
        str(dayChangeFormatted),
        market_cap
    ])

     

print("The following is your personalized investment portfolio model")
print(table)



portfolio_value_formatted = '{:,}'.format(round(portfolio_value,2))
last_updated_formatted = datetime.fromtimestamp(last_updated).strftime('%B, %D, %Y at %I:%M%p')

print("Total portfolio value is " + portfolio_value_formatted)
print ("Last updated on " + last_updated_formatted)

already_hit=[]

while True:
    with open("alerts.txt") as input:
        for line in input: 
            symbolName, alertAmount = line.split()
            symbolName = symbolName.upper()

            URL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD'.format(symbolName)

            response1 = requests.get(URL)
            response1 = response1.json()
            
            prices = response1['RAW'][symbolName]['USD']['PRICE']
            last_updated = response1['RAW'][symbolName]['USD']['LASTUPDATE']
            if prices >= float(alertAmount) and symbolName not in already_hit:
                os.system("say " + name + "hit" + alertAmount)
                last_updated_formatted = datetime.fromtimestamp(last_updated).strftime('%B, %D, %Y at %I:%M%p')
                print (name + " hit " + alertAmount + " on " + last_updated_formatted)
                already_hit.append(symbolName)

    print("it is still running...")
    time.sleep(600)

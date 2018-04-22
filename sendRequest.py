from tradeFormation import operations
import pandas as pd
import numpy as np
import requests
import json

####Здесь мы получим данные через request
r = requests.get('http://192.168.43.46:3000/rawData')
data = r.json()

portfolio = pd.DataFrame({"address" : ["NA1"],
                          "ticker" : ["NA1"],
                          "price" : [50],
                          "quantity" : [50]})   

#newdeals = pd.DataFrame(data[0])
newdeals = pd.DataFrame()
for line in data:
    newrow = pd.DataFrame(line)
    newdeals = newdeals.append(newrow)
newdeals.index = range(len(newdeals))

trade, portfolio = operations(deals = newdeals, portfolio = portfolio)

profitFactor = (trade.profit.sum() - trade.profit.max()) / trade.loc[trade["profit"] < 0].profit.sum()
    
def maxdd(trade):
    MinIndex = np.where(trade.dinamicProfit == trade.dinamicProfit.min())[0][0]
    maxddvalue = trade.iloc[range(MinIndex)].dinamicProfit.max() - trade.dinamicProfit.min()
    return maxddvalue
    
trade = trade.assign(profFactor = profitFactor)
trade = trade.assign(dd = maxdd(trade))
trade = trade.assign(sumprofit = trade.profit.sum())

tradersinfo = trade.to_json(orient = "records")

#tradersResInfo = 
requests.post('http://192.168.43.46:3000/resultData',
              data = tradersinfo,
              headers = {"Content-Type" : "application/json"})

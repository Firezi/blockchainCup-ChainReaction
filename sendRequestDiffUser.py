from tradeFormation import operations
import pandas as pd
import numpy as np
import requests
import time

while True:
####Здесь мы получим данные через request
    r = requests.get('http://192.168.43.47:3000/rawData')
    data = r.json()  
    
    #newdeals = pd.DataFrame(data[0])
    newdeals = pd.DataFrame()
    for line in data:
        newrow = pd.DataFrame(line)
        newdeals = newdeals.append(newrow)
    newdeals.index = range(len(newdeals))
    newdealsALL = newdeals
    uniqUser = set(newdeals.address)
    
    for user in uniqUser:
        newdeals = newdealsALL.loc[newdealsALL["address"] == user]
        newdeals.index = range(len(newdeals))
        portfolio = pd.DataFrame({"address" : ["NA1"],
                              "ticker" : ["NA1"],
                              "price" : [50],
                              "quantity" : [50]}) 
        
        trade, portfolio = operations(deals = newdeals, portfolio = portfolio)
        
        if trade.loc[trade["profit"] < 0].profit.sum() != 0:
            profitFactor = (trade.profit.sum() - trade.profit.max()) / trade.loc[trade["profit"] < 0].profit.sum()
        else:
            profitFactor = trade.profit.sum() - trade.profit.max()
        def maxdd(trade):
            MinIndex = np.where(trade.dinamicProfit == trade.dinamicProfit.min())[0][0]
            if len(trade.iloc[range(MinIndex)]) == 0:
                maxddvalue = 0
            else:
                maxddvalue = trade.iloc[range(MinIndex)].dinamicProfit.max() - trade.dinamicProfit.min()
            return maxddvalue
            
        trade = trade.assign(profFactor = profitFactor)
        trade = trade.assign(dd = maxdd(trade))
        trade = trade.assign(sumprofit = trade.profit.sum())
        trade = trade.assign(avrprofit = trade.dinamicProfit[len(trade) - 1] / len(trade))
        trade = trade.assign(percentWinning = len(trade.loc[trade["profit"] > 0]) / len(trade))
        if trade.dd[0] == 0:
            trade = trade.assign(recovery = trade.dinamicProfit[len(trade) - 1])
        else:
            trade = trade.assign(recovery = trade.dinamicProfit[len(trade) - 1] / trade.dd)
        
        tradersinfo = trade.to_json(orient = "records")
        
        #tradersResInfo = 
        requests.post('http://192.168.43.47:3000/resultData',
                      data = tradersinfo,
                      headers = {"Content-Type" : "application/json"})
    time.sleep(10)
    print("Всё работает, всё ок")

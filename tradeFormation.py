import pandas as pd
import numpy as np
#это получаю на вход (новые операции) (здесь для теста придуманы значения)
newdeals = pd.DataFrame({"ticker" : ["SB", "MTS", "SB"],
                     "price": [228, 1137, 500],
                     "quantity" : [-10, 9, -1],
                     "commission" : [1, 1, 1],
                     "time": ["4/20/18 16:20", "4/20/18 16:25", "4/20/18 16:35"]})

#текущее состояние портфеля/баланс (здесь для теста придуманы значения)
currentportfolio = pd.DataFrame({"ticker" : ["SB", "jmih"],
                                 "quantity" : [15, 9],
                                 "price" : [200, 10]})


def operations(deals, portfolio = pd.DataFrame({"ticker" : [],
                                                "price" : [],
                                                "quantity" : []})):
    trade = pd.DataFrame({"ticker" : [],
                      "diffPrice" : [],
                      "diffQuantity" : [],
                      "profit" : []})
    for i in range(0, len(deals)):
        if any(deals.ticker[i] == portfolio.ticker):
            index = int(np.where(portfolio.ticker == deals.ticker[i])[0][0])
            
            #если происходит операция с одинаковым знаком операции
            #(были куплены и ещё купили)
            if portfolio.quantity[index]*deals.quantity[i] > 0:
                if portfolio.price[index] == deals.price[i]:
                    #если куплены по одинаковой цене, то сложи
                    portfolio.quantity[index] += deals.quantity[i] 
                else:
                    #если по разной цене, то просто добавляет новую строчку того же типа
                    portfolio = portfolio.append(pd.DataFrame({"quantity" : [deals.quantity[i]],
                                                               "price" : [deals.price[i]],
                                                               "ticker": [deals.ticker[i]]}), ignore_index = True)
            else: #если все-таки разные знаки операций            
                #пойдёт в портфель (новое значение)
                portQuantity = portfolio.quantity[index] + deals.quantity[i]  
                portTicker = portfolio.ticker[index]
                
                #уходят в trade
                if deals.quantity[i] > 0: #если покупаем
                    if abs(portfolio.quantity[index]) <= abs(deals.quantity[i]):
                        trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(portfolio.quantity[index])],
                                                           "diffPrice" : [portfolio.price[index] - deals.price[i]],
                                                           "ticker": [deals.ticker[i]],
                                                           "time" : [deals.time[i]]}), ignore_index = True)
                        portfolio.at[index, "price"] = deals.price[i]
                    else:
                        trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(deals.quantity[i])],
                                                           "diffPrice" : [portfolio.price[index] - deals.price[i]],
                                                           "ticker": [deals.ticker[i]],
                                                           "time" : [deals.time[i]]}), ignore_index = True)
                        portfolio.at[index, "price"] = portfolio.price[index]
                else: #если продаём
                    if abs(portfolio.quantity[index]) <= abs(deals.quantity[i]):
                        trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(portfolio.quantity[index])],
                                                           "diffPrice" : [deals.price[i] - portfolio.price[index]],
                                                           "ticker": [deals.ticker[i]],
                                                           "time" : [deals.time[i]]}), ignore_index = True)
                        portfolio.at[index, "price"] = deals.price[i]
                    else:
                        trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(deals.quantity[i])],
                                                           "diffPrice" : [deals.price[i] - portfolio.price[index]],
                                                           "ticker": [deals.ticker[i]],
                                                           "time" : [deals.time[i]]}), ignore_index = True)
                        portfolio.at[index, "price"] = portfolio.price[index]
                portfolio.at[index, "ticker"] = portTicker
                portfolio.at[index, "quantity"] = portQuantity
    
                #если возможно ещё одну trade сделать
                if len(np.where(portfolio.ticker == deals.ticker[i])[0]) > 1:
                    index2 = np.where(portfolio.ticker == deals.ticker[i])[0][1]
                    if portfolio.quantity[index]*portfolio.quantity[index2] < 0:   
                        portQuantity = portfolio.quantity[index2] + portfolio.quantity[index] 
                        portTicker = portfolio.ticker[index]
                        
                        if portfolio.quantity[index] > 0: #если покупаем
                            if abs(portfolio.quantity[index2]) <= abs(portfolio.quantity[index]):
                                trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(portfolio.quantity[index2])],
                                                                   "diffPrice" : [portfolio.price[index2] - portfolio.price[index]],
                                                                   "ticker": [portfolio.ticker[index]],
                                                                   "time" : [deals.time[i]]}), ignore_index = True)
                                portfolio.at[index, "price"] = portfolio.price[index]
                            else:
                                trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(portfolio.quantity[index])],
                                                                   "diffPrice" : [portfolio.price[index2] - portfolio.price[index]],
                                                                   "ticker": [portfolio.ticker[index]],
                                                                   "time" : [deals.time[i]]}), ignore_index = True)
                                portfolio.at[index, "price"] = portfolio.price[index2]
                        else: #если продаём
                            if abs(portfolio.quantity[index2]) <= abs(portfolio.quantity[index]):
                                trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(portfolio.quantity[index2])],
                                                                   "diffPrice" : [portfolio.price[index] - portfolio.price[index2]],
                                                                   "ticker": [portfolio.ticker[index]],
                                                                   "time" : [deals.time[i]]}), ignore_index = True)
                                portfolio.at[index, "price"] = portfolio.price[index]
                            else:
                                trade = trade.append(pd.DataFrame({"diffQuantity" : [abs(portfolio.quantity[index])],
                                                                   "diffPrice" : [portfolio.price[index] - portfolio.price[index2]],
                                                                   "ticker": [portfolio.ticker[index]],
                                                                   "time" : [deals.time[i]]}), ignore_index = True)
                                portfolio.at[index, "price"] = portfolio.price[index2]

                        portfolio.at[index, "ticker"] = portTicker
                        portfolio.at[index, "quantity"] = portQuantity
                        #portfolio.at[index, "price"] = portPrice
                        
                        portfolio = portfolio.drop(index2)
    trade.profit = trade.diffQuantity * trade.diffPrice
    trade = trade.assign(percentProfit = trade.profit / 10000)
    
    trade = trade.assign(dinamicProfit = "NA")
    trade.at[0, "dinamicProfit"] = trade.profit[0]
    for i in range(1, len(trade)):
        trade.at[i, "dinamicProfit"] = trade.profit[i] + trade.dinamicProfit[i - 1]
        
    return trade


###demo
tradedemo = operations(deals = newdeals, portfolio = currentportfolio)

profitFactor = (tradedemo.profit.sum() - tradedemo.profit.max()) / tradedemo.loc[tradedemo["profit"] < 0].profit.sum()

def maxdd(tradedemo):
    MinIndex = np.where(tradedemo.dinamicProfit == tradedemo.dinamicProfit.min())[0][0]
    maxddvalue = tradedemo.iloc[range(MinIndex)].dinamicProfit.max() - tradedemo.dinamicProfit.min()
    return maxddvalue

maxDD = maxdd(tradedemo)

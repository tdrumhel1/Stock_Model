
# coding: utf-8
print (1)
# In[1]:
#Test
def Stock_Data(ticker, start_date, end_date, source = 'google'):

    import pandas.io.data as web
    import datetime
    import pandas as pd
    import numpy as np

    f = web.DataReader(ticker, source, start_date, end_date)
    f['Date'] = pd.to_datetime(f.index,'%m/%d/%y')
    f['date_index'] = ((f['Date'] - f.index.min())/np.timedelta64(1, 'D')).astype(int)
    f['40_Day'] = pd.rolling_mean(f["Close"],40)
    f['80_Day'] = pd.rolling_mean(f["Close"],80)
    f['120_Day'] = pd.rolling_mean(f["Close"],120)
    f['40_Flag'] = np.where(f['Close'] > f['40_Day'], 1, 0)
    f['120_Flag'] = np.where(f['Close'] < f['120_Day'], 1, 0)

    return f

def Transactions(f):

    buy_indicator = 0
    transactions = {}
    Last_Transaction_Index = 0

    #Determining when to Buy and Sell
    for index, row in f.iterrows():
        if row['40_Flag'] == 1 and buy_indicator == 0 and row['date_index'] > 120:
            transactions[row['Date']] = [row['Close'], 'Buy']
            Last_Transaction_Index = row['date_index']
            buy_indicator = 1
        if row['120_Flag'] == 1 and buy_indicator == 1 and row['date_index'] - Last_Transaction_Index > 1:
            transactions[row['Date']] = [row['Close'], 'Sell']
            buy_indicator = 0

    Buy_Total = 0
    Sell_Total = 0
    Buy_Count = 0
    Sell_Count = 0

    #Determining Profit and Total Transactions
    for key in transactions:
        if transactions[key][1] == 'Buy':
            Buy_Total += transactions[key][0]*100
            Buy_Count += 1
        elif transactions[key][1] == 'Sell':
            Sell_Total += transactions[key][0]*100
            Sell_Count += 1

    #Selling Last Purchase if at End of Date Range
    if transactions[max_tran_date][1] == 'Buy':
        Sell_Total += transactions[max_tran_date][0]*100
        Sell_Count += 1

    return Sell_Total - Buy_Total, (Buy_Total/Buy_Count), Buy_Count, Sell_Count, transactions

def Rolling_Average_Intersection(f):

    buy_indicator = 0
    transactions = {}
    Last_Transaction_Index = 0
    Last_Rolling_40 = 10000
    Last_Rolling_120 = 0

    #Determining when to Buy and Sell
    for index, row in f.iterrows():
        if row['40_Day'] > row['120_Day'] and Last_Rolling_40 < row['120_Day'] and buy_indicator == 0 and row['date_index'] > 120:
            transactions[row['Date']] = [row['Close'], 'Buy']
            Last_Transaction_Index = row['date_index']
            buy_indicator = 1
        if row['40_Day'] < row['120_Day'] and Last_Rolling_120 > row['40_Day'] and buy_indicator == 1:
            transactions[row['Date']] = [row['Close'], 'Sell']
            buy_indicator = 0
        Last_Rolling_40 = row['40_Day']
        Last_Rolling_120 = row['120_Day']

    Buy_Total = 0
    Sell_Total = 0
    Buy_Count = 0
    Sell_Count = 0

    #Determining Profit and Total Transactions
    for key in transactions:
        if transactions[key][1] == 'Buy':
            Buy_Total += transactions[key][0]*100
            Buy_Count += 1
        elif transactions[key][1] == 'Sell':
            Sell_Total += transactions[key][0]*100
            Sell_Count += 1
    max_tran_date = max(transactions.keys())

    #Selling Last Purchase if at End of Date Range
    if transactions[max_tran_date][1] == 'Buy':
        Sell_Total += transactions[max_tran_date][0]*100
        Sell_Count += 1

    return Sell_Total - Buy_Total, (Buy_Total/Buy_Count), Buy_Count, Sell_Count, transactions

def Stock_Plot(f, transactions):

    from matplotlib import pyplot as plt

    Dates = f["Date"]
    Close = f["Close"]

    Buy_Dates = [(x,transactions[x][0]) for x in transactions if transactions[x][1] == 'Buy']
    Buy_Dates.sort()
    Sell_Dates = [(x,transactions[x][0]) for x in transactions if transactions[x][1] == 'Sell']
    Sell_Dates.sort()

    plt.plot(Dates, Close)
    plt.scatter(*zip(*Buy_Dates), color = 'b')
    plt.scatter(*zip(*Sell_Dates), color = 'r')

    plt.show()

    return None


# In[3]:

ticker_list = ['VRX','AAPL', 'GOOG','VRX', 'COF','BAC', 'MO', 'D', 'DIS', 'RGR']
Start_Date = '2006-01-01'
End_Date = '2016-08-01'
Profit_By_Stock = []

for ticker in ticker_list:
    f = Stock_Data(ticker, Start_Date, End_Date)
    Profit, Avg_Purch, Buy_Count, Sell_Count, transactions = Rolling_Average_Intersection(f)
    Profit_By_Stock.append((ticker,Profit,Avg_Purch))

summ = 0
avg_purch = 0

for row in Profit_By_Stock:
    summ += row[1]
    avg_purch += row[2]

Profit_By_Stock.append(('Total',summ,avg_purch))
import numpy as np
Profit_By_Stock = np.array(Profit_By_Stock)
print Profit_By_Stock


# In[ ]:

def Taxes_and_Fees(transactions):

    for key in transactions:
        if transactions[key][1] == 'Buy':
            Buy_Total += transactions[key][0]*100
            Buy_Count += 1
        elif transactions[key][1] == 'Sell':
            Sell_Total += transactions[key][0]*100
            Sell_Count += 1
    max_tran_date = max(transactions.keys())

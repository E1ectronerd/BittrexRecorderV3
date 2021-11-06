# -*- coding: utf-8 -*-
# this program was intended to scrape crypto prices for use in machine learning

import csv
import datetime
import time
import os.path
from datetime import datetime
import BittrexAPIv3
    

# list of all coins to poll bittrex
#coinList = ['USDT-ETH','USDT-BTC', "USDT-LTC"]
coinList = ['ETH-USDT','BTC-USDT', "LTC-USDT"]
# list of data points for each coin
dataList = ['timeStamp', 'High','Low','Volume','PriceLast','BaseVolume',
            'PriceAsk','PriceBid','PrevDay']

# list of processed data for NN training
processedDataList = ['timeStamp', 'HighPriceFB', 'LowPriceFB', 'High', 'Low',
                     'Volume', 'VolLngM', 'VolLngB', 'VolSrtM', 'VolSrtB', 
                     'PriceLast', 'BaseVolume', 'PriceAsk', 'AskLngM',
                     'AskLngB','AskSrtM', 'AskSrtB', 'PriceBid', 'BidLngM',
                     'BidLngB',  'BidSrtM',  'BidSrtB',
                     'PrevDay', 'totBuyQant', 'TBQlngB',
                     'TBQlngM', 'TBQsrtB', 'TBQsrtM', 'totSellQant', 
                     'TSQlngB', 'TSQlngM', 'TSQsrtB', 'TSQsrtM', 'end']




# list of processed data for NN training
simpleDataList = ['HighPriceFB', 'LowPriceFB', 'High', 'Low',
                  'Volume', 'PriceLast', 'BaseVolume', 'PriceAsk', 'PriceBid',
                  'PrevDay', 'totBuyQant', 'totSellQant', 'end']


def getCoinSummary(coin):   

    tickerBool, json_ticker = BittrexAPIv3.get_ticker(coin)

    summaryBool, json_summary = BittrexAPIv3.get_dailySummary(coin)

    if (tickerBool == True) and (summaryBool == True):

        if 'high' in json_summary:
            High = json_summary['high']
        else:
            High = '-1'

        if 'low' in json_summary:
            Low = json_summary['low']
        else:
            Low = '-1'

        if 'volume' in json_summary:
            Volume = json_summary['volume']
        else:
            Volume = '-1'

        if 'lastTradeRate' in json_ticker:
            PriceLast = json_ticker['lastTradeRate']
        else:
            PriceLast = '-1'

        if 'quoteVolume' in json_summary:
            BaseVolume = json_summary['quoteVolume']
        else:
            BaseVolume = '-1'

        if 'updatedAt' in json_summary:
            time = json_summary['updatedAt']
        else:
            time = '-1'

        if 'askRate' in json_ticker:
            PriceAsk = json_ticker['askRate']
        else:
            PriceAsk = '-1'

        if 'bidRate' in json_ticker:
            PriceBid = json_ticker['bidRate']
        else:
            PriceBid = '-1'

        PrevDay = '-1'
        tempSingleCoinData.append(time)
        tempSingleCoinData.append(High)
        tempSingleCoinData.append(Low)
        tempSingleCoinData.append(Volume)
        tempSingleCoinData.append(PriceLast)
        tempSingleCoinData.append(BaseVolume)
        tempSingleCoinData.append(PriceAsk)
        tempSingleCoinData.append(PriceBid)
        tempSingleCoinData.append(PrevDay)

    elif tickerBool == True:
        High = '-1'
        Low = '-1'
        Volume = '-1'

        if 'lastTradeRate' in json_ticker:
            PriceLast = json_ticker['lastTradeRate']
        else:
            PriceLast = '-1'

        BaseVolume = '-1'
        time = '-1'

        if 'askRate' in json_ticker:
            PriceAsk = json_ticker['askRate']
        else:
            PriceAsk = '-1'

        if 'bidRate' in json_ticker:
            PriceBid = json_ticker['bidRate']
        else:
            PriceBid = '-1'

        PrevDay = '-1'
        tempSingleCoinData.append(time)
        tempSingleCoinData.append(High)
        tempSingleCoinData.append(Low)
        tempSingleCoinData.append(Volume)
        tempSingleCoinData.append(PriceLast)
        tempSingleCoinData.append(BaseVolume)
        tempSingleCoinData.append(PriceAsk)
        tempSingleCoinData.append(PriceBid)
        tempSingleCoinData.append(PrevDay)

    else:
        print("**failed to fetch Summary**")
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')
        tempSingleCoinData.append('-1')

                        
def PollAPI(coin):
    del tempSingleCoinData [:]
    getCoinSummary(coin)
                                
    
def GetCoinListData():
    global tempCoinListData
    for coin in coinList:
        PollAPI(coin)
        tempCoinListData.extend(tempSingleCoinData)
        #print(tempSingleCoinData)
        
def buildHeadder():
    for coin in coinList:
        for dataPt in dataList:
            tempStr = ""
            tempStr += coin
            tempStr += "-"
            tempStr += dataPt
            header.append(tempStr)
            
    
def WriteDailyFile( path ):
    global tempCoinListData
    date = datetime.today().strftime('%Y-%m-%d')
    #print(date)
    fileName = ""    
    fileName += "NNrec-"
    fileName += date
    fileName += ".csv"
    
    cntr = 1441 # Number of minutes in a day pluss 1 
    
    with open(os.path.dirname(__file__) + path + fileName, 'w') as csvfile:
        lineWriter = csv.writer(csvfile, dialect='excel', delimiter=',')
        buildHeadder()
        lineWriter.writerow(header) 
        
        while cntr > 0 :  # one day timer here
            start = datetime.now()
            GetCoinListData()
            lineWriter.writerow(tempCoinListData)        
            csvfile.flush()
            #print(tempCoinListData)
            del tempCoinListData [:]
            cntr -= 1
            procTime = datetime.now()

            exec_time = procTime - start

            try:
                time.sleep(60 - exec_time.total_seconds())

            except Exception:
                time.sleep(60)
                print(Exception)
                print("time Calc Error: ", "exec_time: ", exec_time, " start: ", start)

            
        csvfile.close
        
        
##=============================================##
# USDT-ETH
# USDT-BTC
# USDT-LTC
header = []
#coinList and dataList defined in dataDefs.py

tempCoinListData = []    
tempSingleCoinData = []    
if __name__ == '__main__':

    #print("path: ../../../Public/")
    #print("Enter File path for file export:")
    #path = input()
    #print(os.path.dirname(__file__) )
    
    path = '../../../Public/CryptoRec/'
    while 1:
        WriteDailyFile( path )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




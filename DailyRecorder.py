# -*- coding: utf-8 -*-
# this program was intended to scrape crypto prices for use in machine learning

import csv
import json
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
        High = json_summary['high']
        Low = json_summary['low']
        Volume = json_summary['volume']
        PriceLast = json_ticker['lastTradeRate']
        BaseVolume = json_summary['quoteVolume']
        time = json_summary['updatedAt']
        PriceAsk = json_ticker['askRate']
        PriceBid = json_ticker['bidRate']
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
        PriceLast = json_ticker['lastTradeRate']
        BaseVolume = '-1'
        time = '-1'
        PriceAsk = json_ticker['askRate']
        PriceBid = json_ticker['bidRate']
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
            start = time.time()
            
            GetCoinListData()
            lineWriter.writerow(tempCoinListData)        
            csvfile.flush()
            #print(tempCoinListData)
            del tempCoinListData [:]
            cntr -= 1
            procTime = time.time()
            time.sleep(60 - (procTime - start))
            
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




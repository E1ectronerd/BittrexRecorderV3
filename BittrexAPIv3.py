#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 17:53:24 2021

@author: leviathan
@source: https://github.com/hanhha/bittrex/blob/master/bittrex.py
"""
import requests



# Gets Ticker data for market
def get_ticker(market):
    # Response
    # {
    #  "symbol": "string",
    #  "lastTradeRate": "number (double)",
    #  "bidRate": "number (double)",
    #  "askRate": "number (double)"
    # }
    reqUrl = 'https://api.bittrex.com/v3/markets/{marketSymbol}/ticker'
    reqUrl = reqUrl.format(marketSymbol = market)

    try:
        raw_dict = requests.get(reqUrl).json()
        if 'symbol' in raw_dict:
            return True, raw_dict
        else:
            return False, raw_dict
    except requests.ConnectionError:
        print("Connection Error: get_ticker")
        return False, {}

# get 24 hr rolling average for market
def get_dailySummary(market):
    # Response
    #{
    #    "symbol": "string",
    #    "high": "number (double)",
    #    "low": "number (double)",
    #    "volume": "number (double)",
    #    "quoteVolume": "number (double)",
    #    "percentChange": "number (double)",
    #    "updatedAt": "string (date-time)"
    #}

    reqUrl = 'https://api.bittrex.com/v3/markets/{marketSymbol}/summary'
    reqUrl = reqUrl.format(marketSymbol=market)

    try:
        raw_dict = requests.get(reqUrl).json()
        if 'symbol' in raw_dict:
            return True, raw_dict
        else:
            return False, raw_dict
    except requests.ConnectionError:
        print("Connection Error: get_dailySummary")
        return False, {}

# Returns all available markets
#
#
def get_markets():
    reqUrl = 'https://api.bittrex.com/v3/markets'
    return requests.get(reqUrl).json()


#
#
# Test code
if __name__ == '__main__':
    print("Test Starting")
    #get_markets()
    resultbool, json = get_ticker('ETH-USDT')
    print("test")
    print(json['lastTradeRate'])

    if resultbool == True:
        print("BOOL check worked")
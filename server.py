# -*- coding: utf-8 -*-
import os
import requests

from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify
from yahoo_finance import Share
from googlefinance import getQuotes
import operator
from bs4 import BeautifulSoup
from urllib import urlopen
 

app = Flask(__name__)


#Temporary ticker symbol arrays
etf_symbols = ["SLYG", 'IWO', 'IYT', 'ITA', 'IJT', 'SOXX', 'VBK']
stock_symbols= ['ADBE', 'YHOO', 'AAPL', 'WMY', 'ROL', 'GSAT', 'PIRS', 'NVDA', 'AMZN', 'ABT', 'GOOG']

#Return the stock names with the lowest ratio of price–earnings ratio
def get_value_investing_symbols():
      stocks = []

      #Loop each stock and generate an array with (stock_name, price-earnings ratio) tuples
      for s in stock_symbols:
            stock = Share(s)
            pe_ratio = stock.get_price_earnings_ratio()
           
            if pe_ratio is not None:
                  stocks.append((s, float(pe_ratio)))
          
      #sort the array by price–earnings ratio(lowest first)
      stocks = sorted(stocks, key = operator.itemgetter(1))


      #return the recommended symbols
      return [stocks[0][0], stocks[1][0], stocks[2][0]]



#Return the top 3 etfs (highest price)
def get_index_investing_data():
      etfs = [];
    
      return ""



#TODO: How to divide better? I'm just dividing them equally
def divide_money(stocks, investment):
      divide_dict = {}
      inv_per_stock = investment/ len(stocks);

      for symbol in stocks:
            stock = Share(symbol)
            divide_dict[symbol] = int(inv_per_stock / float(stock.get_price()))


      return divide_dict



#Scrape finance.yahoo.com to get historical data for each suggested stock/etf
def get_historical_data(symbol, investment):
      history_data = []
      historyUrl = 'https://finance.yahoo.com/quote/' + symbol + '/history/'
      historyPage = urlopen(historyUrl)
      soup = BeautifulSoup(historyPage, "html.parser")
      rows = soup.findAll("tr", {"class": "BdT"})  

      #First 5 rows = data of last 5 days
      for x in range(0, 5):
            #Table data span order: date, open, high, low, close, adjClose, volume
            spans = rows[x].find_all("span")
            day_data = {
                  "Date": spans[0].get_text(), 
                  "Open": float(spans[1].get_text()), 
                  "High": float(spans[2].get_text()), 
                  "Low": float(spans[3].get_text()), 
                  "Close": float(spans[4].get_text()), 
                  "AdjClose": float(spans[5].get_text()), 
                  "Volume": spans[6].get_text(),
                  "Symbol": symbol
            }

            history_data.append(day_data)

      return history_data



@app.route('/stock_data', methods=['POST'])
def stock_data():
      print request.json["strategies"]
      print request.json["investment"]

      investment = float(request.json["investment"])
      result = {}
      result["history_data"] = []

      #TODO: For now, this call is only returning value investing data.
      suggested_stock_symbols = get_value_investing_symbols()
      for s in suggested_stock_symbols:
            result["history_data"].append(get_historical_data(s, request.json["investment"]))
      

      #Divide investment
      result["divide_data"] = divide_money(suggested_stock_symbols, investment)
      return jsonify(result)



@app.route('/', methods=['GET'])
def render_main_page():
      return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
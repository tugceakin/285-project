# -*- coding: utf-8 -*-
import operator
from datetime import datetime, timedelta

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

from yahoo_finance import Share

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app, session_options={'autocommit': True})

#Return the stock names with the lowest ratio of price–earnings ratio
def get_value_investing_symbols():
      from db import Symbol
      stocks = []

      #Loop each stock and generate an array with (stock_name, price-earnings ratio) tuples
      for s in Symbol.query.filter(Symbol.symbol_type == 'STOCK'):
            stock = Share(s.symbol)
            pe_ratio = stock.get_price_earnings_ratio()
            if pe_ratio is not None:
                  stocks.append((s, float(pe_ratio)))

      #sort the array by price–earnings ratio(lowest first)
      stocks = sorted(stocks, key = operator.itemgetter(1))


      #return the recommended symbols
      return [stocks[0][0], stocks[1][0], stocks[2][0]]


#Return the top 3 etfs (highest price)
def get_index_investing_data():
      from db import Symbol
      from data import get_trend
      recommendation = []
      for s in Symbol.query.filter(db.and_(
                  Symbol.symbol_type == 'ETF',
                  Symbol.index == True
      )):
            data = [x.close for x in s.get_historical_data_monthly()]
            trend = get_trend(data)
            if trend > 0:
                  recommendation.append((s, trend))
      recommendation.sort(key=operator.itemgetter(1))
      return [recommendation[0][0], recommendation[1][0], recommendation[2][0]]


#Return specific 3 quality stock options
def get_quality_investing_symbols():
      from db import Symbol
      quality_stocks = []

      # Only get specific quality stocks
      for s in db.session.query(Symbol).filter(Symbol.quality == True):
            stock = Share(s.symbol)
            pe_ratio = stock.get_price_earnings_ratio()
            if pe_ratio is not None:
                  quality_stocks.append((s, float(pe_ratio)))

      #Sort by highest price earnings ratio
      quality_stocks.sort(key=operator.itemgetter(1), reverse=True)

      #Return top 3
      return [quality_stocks[0][0], quality_stocks[1][0], quality_stocks[2][0]]


#Return specific 3 ethical stock options
def get_ethical_investing_symbols():
      from db import Symbol
      ethical_stocks = []

      # Only get specific ethical stocks
      for s in db.session.query(Symbol).filter(Symbol.ethical == True):
            stock = Share(s.symbol)
            pe_ratio = stock.get_price_earnings_ratio()
            if pe_ratio is not None:
                  ethical_stocks.append((s, float(pe_ratio)))

      # Sort by highest price earnings ratio
      sorted(ethical_stocks, key=operator.itemgetter(1), reverse=True)

      # Return top 3
      return [ethical_stocks[0][0], ethical_stocks[1][0], ethical_stocks[2][0]]


#TODO: How to divide better? I'm just dividing them equally
def divide_money(stocks, investment):
      divide_dict = {}
      inv_per_stock = investment/ len(stocks);

      for symbol in stocks:
            stock = Share(symbol.symbol)
            divide_dict[symbol.symbol] = int(inv_per_stock / float(stock.get_price()))


      return divide_dict


@app.route('/stock_data', methods=['POST'])
def stock_data():
      print request.json["strategies"]
      print request.json["investment"]

      investment = float(request.json["investment"])
      strategies = request.json["strategies"];
      result = {}
      result["history_data"] = []
      suggested_stock_symbols = []

      if "Index Investing" in strategies:
            #Concatenate two lists
            suggested_stock_symbols = suggested_stock_symbols + get_index_investing_data() 

      if "Value Investing" in strategies:  
            suggested_stock_symbols = suggested_stock_symbols + get_value_investing_symbols()
            
      if "Quality Investing" in strategies:  
            suggested_stock_symbols = suggested_stock_symbols + get_quality_investing_symbols()
            
      if "Ethical Investing" in strategies:  
            suggested_stock_symbols = suggested_stock_symbols + get_ethical_investing_symbols()

      for s in suggested_stock_symbols:
            result["history_data"].append([x.to_json() for x in s.get_historical_data()])

      #Divide investment
      result["divide_data"] = divide_money(suggested_stock_symbols, investment)
      return jsonify(result)



@app.route('/', methods=['GET'])
def render_main_page():
      return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

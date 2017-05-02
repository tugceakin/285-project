import os
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify
from yahoo_finance import Share

app = Flask(__name__)


def past_n_days(n):
      date_arr = []
      for i in range(1, n):
            day = datetime.now() - timedelta(days=i)
            date_arr.append(day.isoformat())
      print date_arr

def get_historical_data(stock, n):
      date_arr = []
      for i in range(1, n+1):
            day = datetime.now() - timedelta(days=i)
            date_arr.append(day.strftime("%Y-%m-%d"))

      print date_arr
      return stock.get_historical(date_arr[n-1], date_arr[0]) #start date, end date


@app.route('/stock_data', methods=['POST'])
def stock_data():
      print request.json["strategies"]
      print request.json["investment"]
      symbol = "ADBE"
      stock = Share("ADBE")
      

      data  = get_historical_data(stock, 7)
      return jsonify(data)

@app.route('/', methods=['GET'])
def render_main_page():
      return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
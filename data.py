from bs4 import BeautifulSoup
from urllib import urlopen
from dateutil.parser import parse as parse_date
from numpy import arange
from scipy import stats

def scrape_historical_data(symbol, monthly=False):
      history_data = []
      if monthly:
            history_url = 'https://finance.yahoo.com/quote/' + symbol + \
            '/history/?interval=1mo&frequency=1mo'
            r = range(0, 15)
      else:
            history_url = 'https://finance.yahoo.com/quote/' + symbol + '/history/'
            r = range(0, 5)
      history_page = urlopen(history_url)
      soup = BeautifulSoup(history_page, "html.parser")
      rows = soup.findAll("tr", {"class": "BdT"})

      #First 5 rows = data of last 5 days
      for x in r:
            #Table data span order: date, open, high, low, close, adjClose, volume
            spans = rows[x].find_all("span")
            if not len(spans) == 7:
                  continue
            day_data = {
                  "date": parse_date(spans[0].get_text()).date(),
                  "open": float(spans[1].get_text()),
                  "high": float(spans[2].get_text()),
                  "low": float(spans[3].get_text()),
                  "close": float(spans[4].get_text()),
                  "adj_close": float(spans[5].get_text()),
                  "volume": spans[6].get_text(),
            }

            history_data.append(day_data)

      return history_data

def get_trend(values):
      xi = arange(0, len(values))
      slope, intercept, r_value, p_value, std_err = stats.linregress(xi, values)
      return slope

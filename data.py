from bs4 import BeautifulSoup
from urllib import urlopen
from dateutil.parser import parse as parse_date

def scrape_historical_data(symbol):
      history_data = []
      history_url = 'https://finance.yahoo.com/quote/' + symbol + '/history/'
      history_page = urlopen(history_url)
      soup = BeautifulSoup(history_page, "html.parser")
      rows = soup.findAll("tr", {"class": "BdT"})

      #First 5 rows = data of last 5 days
      for x in range(0, 5):
            #Table data span order: date, open, high, low, close, adjClose, volume
            spans = rows[x].find_all("span")
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

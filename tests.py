import unittest

from data import get_trend
from flask_sqlalchemy import SQLAlchemy
from data import scrape_historical_data
from mock import patch

import app

class TestTrends(unittest.TestCase):

    def test_upward_trend(self):
        self.assertGreater(get_trend([1, 2, 3, 4, 5]), 0)

    def test_downward_trend(self):
        self.assertLess(get_trend([5, 4, 3, 2, 1]), 0)

    def test_recovering_trend(self):
        self.assertGreater(get_trend([5, 2, 3, 4, 5]), 0)

    def test_bellcurve_trend(self):
        self.assertLessEqual(get_trend([2, 3, 4, 3, 2]), 0)

    def test_inverse_bellcurve_trend(self):
        self.assertLessEqual(get_trend([4, 3, 2, 4]), 0)


class TestCaching(unittest.TestCase):

    def setUp(self):
        from init_db import init_db
        self._old_db = app.db
        self._old_db_uri = app.app.config['SQLALCHEMY_DATABASE_URI']
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' #in memory
        app.db = SQLAlchemy(app.app)
        init_db()

    @patch('db.scrape_historical_data', side_effect=scrape_historical_data)
    def test_cached_historical_results(self, scrape_mock):
        from db import Symbol
        s = Symbol.query.filter(Symbol.symbol=='VBK').first()
        # we expect scraping the first time
        s.get_historical_data_monthly()
        self.assertEqual(scrape_mock.call_count, 1)
        s.get_historical_data_monthly()
        # we expect no scraping this time
        self.assertEqual(scrape_mock.call_count, 1)

    def tearDown(self):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = self._old_db_uri
        app.db = self._old_db



if __name__ == "__main__":
    unittest.main()

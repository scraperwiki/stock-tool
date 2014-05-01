#!/usr/bin/env python
# encoding: utf-8
import datetime
import unittest

import mock
import pandas as pd
import pandas_finance

from pandas.util.testing import assert_frame_equal
from nose.tools import assert_equal
from freezegun import freeze_time


class GetStockTestCase(unittest.TestCase):
    @mock.patch('pandas_finance.web.DataReader')
    def test_get_stock_called_correctly(self, mock_datareader):
        start = datetime.datetime(1999, 4, 3, 0, 0)
        end = datetime.datetime(2005, 2, 5, 0, 0)
        pandas_finance.get_stock('AAPL', start, end)
        mock_datareader.assert_called_with('AAPL', 'yahoo', start, end)

    def test_get_required_tickers_parses_tickers_with_newline(self):
        m = mock.mock_open(read_data='TWTR,FB,AAPL,MSFT\n')
        textfile = None  # Only used to provide valid argument.
        with mock.patch('pandas_finance.open', m, create=True):
            result = pandas_finance.get_required_tickers(textfile)
        assert_equal('TWTR,FB,AAPL,MSFT', result)


class ScrapeStockTestCase(unittest.TestCase):
    def setUp(self):
        """Run once before each test in this test class."""
        self.start = datetime.datetime(2014, 04, 29).date()
        self.end = self.start

        input_values = {'Volume': [12033400],
                        'Adj Close': [592.33],
                        'High': [595.98],
                        'Low': [589.51],
                        'Close': [592.33],
                        'Open': [593.74]}
        index_label = [self.start]
        input_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
        self.input_frame = pd.DataFrame(input_values,
                                        columns=input_columns,
                                        index=index_label)
        self.input_frame.index.name = 'Date'

        output_values = input_values
        # get_stock converts datetime to isoformat string.
        output_values['Date'] = '2014-04-29'
        output_values['Stock'] = 'AAPL'
        output_columns = ['Date'] + input_columns + ['Stock']
        self.output_frame = pd.DataFrame(output_values, columns=output_columns)

    @mock.patch('pandas_finance.write_frame_to_sql')
    @mock.patch('pandas_finance.get_stock')
    def test_scrape_stock_gives_a_valid_frame(self, mock_get_stock,
                                              mock_write_frame):
        mock_get_stock.return_value = self.input_frame
        pandas_finance.scrape_stock('AAPL', self.start, self.end)
        # Hacky workaround:
        # Can't seem to use mock.assert_called_with; problem when comparing
        # dataframes, grab argument directly and compare it to expected frame.
        frame_called_with = mock_write_frame.call_args_list[0][0][0]
        assert_frame_equal(self.output_frame, frame_called_with)


class InstallCrontabTestCase(unittest.TestCase):
    pass


class GetDatesTestCase(unittest.TestCase):
    @freeze_time('2014-04-10 15:05:05')
    def test_get_dates(self):
        start, end = pandas_finance.get_dates()
        assert_equal(datetime.datetime(1900, 1, 1, 0, 0), start)
        assert_equal(datetime.datetime.today(), end)


class MainTestCase(unittest.TestCase):
    def setUp(self):
        patcher1 = mock.patch('pandas_finance.sqlite3.connect')
        self.mock_sqlite3_connect = patcher1.start()
        self.addCleanup(patcher1.stop)

        patcher2 = mock.patch('pandas_finance.get_required_tickers')
        self.mock_get_required_tickers = patcher2.start()
        self.mock_get_required_tickers.return_value = 'TWTR,FB,AAPL'
        self.addCleanup(patcher2.stop)

        patcher3 = mock.patch('pandas_finance.scrape_stock')
        self.mock_scrape_stock = patcher3.start()
        self.addCleanup(patcher3.stop)

        patcher4 = mock.patch('pandas_finance.update_status')
        self.mock_update_status = patcher4.start()
        self.addCleanup(patcher4.stop)

        patcher5 = mock.patch('pandas_finance.install_crontab')
        self.mock_install_crontab = patcher5.start()
        self.addCleanup(patcher5.stop)

        patcher6 = mock.patch('pandas_finance.get_dates')
        self.mock_get_dates = patcher6.start()
        self.addCleanup(patcher6.stop)

        self.start_date = datetime.datetime(1900, 1, 1, 0, 0)
        self.end_date = datetime.datetime(2013, 10, 20, 10, 20, 23, 1234)
        self.mock_get_dates.return_value = self.start_date, self.end_date

    def test_get_dates_call(self):
        pandas_finance.main('tickers.txt')
        self.mock_get_dates.assert_called_with()

    def test_sqlite3_connect_call(self):
        pandas_finance.main('tickers.txt')
        self.mock_sqlite3_connect.assert_called_with('scraperwiki.sqlite')

    def test_database_execute_call(self):
        sqlite_execute_mock = mock.Mock(name='RETURNMOCK')
        self.mock_sqlite3_connect.return_value = sqlite_execute_mock
        pandas_finance.main('tickers.txt')
        expected_call = 'drop table if exists stocks;'
        sqlite_execute_mock.execute.assert_called_with(expected_call)

    def test_get_required_tickers_call(self):
        pandas_finance.main('tickers.txt')
        self.mock_get_required_tickers.assert_called_with('tickers.txt')

    def test_scrape_stock_calls(self):
        pandas_finance.main('tickers.txt')
        expected_calls = []
        for stock in ['TWTR', 'FB', 'AAPL']:
            expected_calls.append(mock.call(stock, self.start_date,
                                            self.end_date))
        self.mock_scrape_stock.assert_has_calls(expected_calls)

    def test_update_status_called(self):
        pandas_finance.main('tickers.txt')
        self.mock_update_status.assert_called_with('stocks')

    def test_install_crontab_called(self):
        pandas_finance.main('tickers.txt')
        self.mock_install_crontab.assert_called_with()

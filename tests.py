#!/usr/bin/env python
# encoding: utf-8
import datetime
import unittest

import mock

from nose.tools import assert_equal, assert_is_instance
from pandas_finance import get_stock, get_required_tickers

class PandasFinanceTestCase(unittest.TestCase):
    @mock.patch('pandas_finance.web.DataReader')
    def test_get_stock_called_correctly(self, mock_datareader):
        mock_datareader()
        start = datetime.datetime(1999, 4, 3, 0, 0)
        end = datetime.datetime(2005, 2, 5, 0, 0)
        get_stock('AAPL', start, end)
        mock_datareader.assert_called_with('AAPL', 'yahoo', start, end)

    def test_get_required_tickers_parses_tickers_with_newline(self):
        m = mock.mock_open(read_data='TWTR,FB,AAPL,MSFT\n')
        textfile = None  # only used to provide valid argument
        with mock.patch('pandas_finance.open', m, create=True):
            result = get_required_tickers(textfile)
        assert_equal('TWTR,FB,AAPL,MSFT', result)

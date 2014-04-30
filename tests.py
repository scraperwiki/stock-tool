#!/usr/bin/env python
# encoding: utf-8
import datetime
import unittest

import mock

from nose.tools import assert_equal, assert_is_instance

from pandas_finance import get_stock

class PandasFinanceTestCase(unittest.TestCase):
    @mock.patch('pandas_finance.web.DataReader')
    def test_get_stock_called_correctly(self, mock_datareader):
        mock_datareader()
        start = datetime.datetime(1999, 4, 3, 0, 0)
        end = datetime.datetime(2005, 2, 5, 0, 0)
        get_stock('AAPL', start, end)
        mock_datareader.assert_called_with('AAPL', 'yahoo', start, end)

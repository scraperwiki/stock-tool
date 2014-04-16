#!/usr/bin/env python
""" pandas_finance.

Usage:
    pandas_finance.py STOCKS START_DATE END_DATE

Arguments:
    STOCKS     comma separated stock ticker symbols, e.g. FB,TWTR
"""
import datetime
import sqlite3
import sys

import pandas.io.data as web
import pandas.io.sql as sql


def get_stock(stock, start, end):
    """
    Return data frame of Yahoo! Finance data for stock.

    Takes stock name and start and end dates as datetimes.
    """
    return web.DataReader(stock, 'yahoo', start, end)


def scrape_stock(stock, start, end):
    """
    Write SQLite table of stock data from Yahoo! Finance

    Take a stock name and start and end dates as datetimes.
    """
    sqlite_db.execute("drop table if exists {};".format(stock))
    frame = (get_stock(stock, start, end))
    # make Date not an index so it appears in table
    frame = frame.reset_index()
    # force Date datetime to string
    frame[['Date']] = frame[['Date']].applymap(lambda x: x.isoformat())
    sql.write_frame(frame, stock, sqlite_db)


def parse_wanted_stocks(stocks_string):
    """
    Take comma-separated string of stocks; return list of strings.
    >>> parse_wanted_stocks('TWTR,FB')
    ['TWTR', 'FB']
    >>> parse_wanted_stocks('TWTR')
    ['TWTR']
    """
    return stocks_string.split(',')


def main():
    """
    Save stock ticker data from Yahoo! Finance to sqlite.
    """
    # Yahoo: "Historical prices typically do not go back further than 1970"
    start = datetime.datetime(1900, 1, 1, 0, 0)
    end = datetime.datetime.today()
    global sqlite_db
    sqlite_db = sqlite3.connect("scraperwiki.sqlite")
    for ticker in parse_wanted_stocks(sys.argv[1]):
        scrape_stock(ticker, start, end)

if __name__ == '__main__':
    main()

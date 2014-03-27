#!/usr/bin/env python
import datetime
import sqlite3
import pandas.io.data as web
import pandas.io.sql as sql


def get_stock(stock, start, end):
    """
    Return data frame of Yahoo Finance data for stock.

    Takes stock name and start and end dates as datetimes.
    """
    return web.DataReader(stock, 'yahoo', start, end)

def scrape_stock(stock, start, end):
    sqlite_db.execute("drop table if exists {};".format(stock))
    frame = (get_stock(stock, start, end))
    # make Date not an index so it appears in table
    frame = frame.reset_index()
    # force Date datetime to string
    frame[['Date']] = frame[['Date']].applymap(lambda x: x.isoformat())
    sql.write_frame(frame, stock, sqlite_db)

def main():
    global sqlite_db
    sqlite_db = sqlite3.connect("scraperwiki.sqlite")
    # arbitrary start
    start = datetime.datetime(2014, 3, 1)
    end = datetime.datetime.today()
    for ticker in ['TWTR', 'FB']:
        scrape_stock(ticker, start, end)
    
if __name__ == '__main__':
    main()

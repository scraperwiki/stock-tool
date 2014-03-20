#!/usr/bin/env python
import datetime

import scraperwiki
import numpy
import pandas.io.data as web


def get_stock(stock, start, end, service):
    """
    Return data frame of finance data for stock.

    Takes start and end datetimes, and service name of 'google' or 'yahoo'.
    """
    return web.DataReader(stock, service, start, end)


def parse_finance_frame(stock, start, end, service='google'):
    """
    Return rows of dicts from a finance data frame for scraperwiki.sqlite.

    service can also be 'yahoo', start and end are datetimes.
    """
    frame = get_stock(stock, start, end, service)
    rows = []
    for idx in range(len(frame)):
        current_row_as_dict = frame.ix[idx].to_dict()
        # have to convert dates because these are Pandas timestamps and
        # dumptruck doesn't support them
        current_row_as_dict['Date'] = frame.index[idx].to_datetime()
        current_row_as_dict['Stock'] = stock
        # horrible hack because data values are numpy.float64 and dumptruck
        # doesn't support them
        for key in current_row_as_dict:
            if isinstance(current_row_as_dict[key], numpy.float64):
                current_row_as_dict[key] = float(current_row_as_dict[key])
        rows.append(current_row_as_dict)
    return rows


def main():
    """
    Dump stock data into scraperwiki.sqlite using pandas.io.data.
    """
    # arbitrary start chosen
    start = datetime.datetime(2014, 3, 1)
    end = datetime.datetime.today()

    stock_list = ['TWTR', 'FB']
    rows = []
    for stock in stock_list:
        rows.extend(parse_finance_frame(stock, start, end))
    scraperwiki.sqlite.save(data=rows, unique_keys=['Stock', 'Date'])

if __name__ == '__main__':
    main()

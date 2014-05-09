#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals
import codecs

import dshelpers
import lxml


def get_yahoo_ticker_xml():
    """ Return Yahoo! Finance ticker company details as XML. """
    url = "http://query.yahooapis.com/v1/public/yql?q=" \
          "select%20*%20from%20yahoo.finance.industry%20where%20id%20in%20" \
          "(select%20industry.id%20from%20yahoo.finance.sectors)&" \
          "env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    return dshelpers.download_url(url)


def yield_ticker_info_from_csv(xml):
    """ Extract symbols and company names from Yahoo! ticker XML. """
    xml_tree = lxml.etree.parse(xml)
    results = xml_tree.xpath('//company')
    for result in results:
        industry = '"' + result.getparent().get('name') + '"'
        name = '"' + result.get('name') + '"'
        yield ','.join([name, result.get('symbol'), industry])


def write_header(fobj):
    """ Write header row to ticker CSV. """
    fobj.write('company name,symbol,industry\n')


def write_csv(xml):
    """ Write header row and company info to CSV. """
    with codecs.open('/home/http/ticker_info.csv', 'w', 'utf-8') as f:
        write_header(f)
        for company_info in yield_ticker_info_from_csv(xml):
            f.write(company_info + '\n')


def main():
    dshelpers.install_cache()
    xml = get_yahoo_ticker_xml()
    write_csv(xml)


if __name__ == '__main__':
    main()

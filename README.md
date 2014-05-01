# pandas_finance
Small script to demonstrate using pandas' DataReader to grab finance data and
store it in SQLite using the scraperwiki module.

Install requirements with `pip install -r requirements.txt`

Run Python tests via `doctest` and `nosetests`.

This is flaky on boxes; Yahoo! Finance worked initially on boxes and locally,
but then stopped working (service down/blocking me?); Google's stock data
didn't seem to be accessible from a box, though worked locally.

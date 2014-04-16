# pandas_finance
Toolified version requires bootstrap-datepicker to be cloned inside tool/http.

Confusingly there are several libraries with this name; get this one:
https://github.com/eternicode/bootstrap-datepicker

Small script to demonstrate using pandas' DataReader to grab finance data and
store it in SQLite using the scraperwiki module.

Install requirements with `pip install -r requirements.txt`

This is flaky on boxes; Yahoo! Finance worked initially on boxes and locally,
but then stopped working (service down/blocking me?); Google's stock data
didn't seem to be accessible from a box, though worked locally.

var param_from_input = function(css) {
    return scraperwiki.shellEscape($(css).val())
}

var runScraper = function() {
  $(this).attr('disabled', true)
  $(this).addClass('loading').html('Scraping&hellip;')
  var stocks = param_from_input('#stocks_input')
  var echoCommand = ['echo -n', stocks, '>', '/home/http/tickers.txt'].join(' ')
  scraperwiki.exec(echoCommand)
  var command = 'python tool/pandas_finance.py tickers.txt'
  scraperwiki.dataset.name("Stock prices of " + $('#stocks_input').val())
  scraperwiki.exec(command, getStocksSuccess)
}

var getStocksSuccess = function(data) {

    $('#submitBtn').attr('disabled', false)

  if (data.indexOf('File "tool/pandas_finance.py"') != -1) {

    scraperwiki.alert('Could not retrieve stock tickers.', "Check your tickers are valid and comma-separated, then try again.<br>If problems persist, it may be an issue with the stock service; please try again later.", true)
    $('#submitBtn').removeClass('loading').html('<i class="icon-remove"></i> Error')
    $('#submitBtn').removeClass('btn-primary').addClass('btn-danger')

    setTimeout(function() {
      $('#submitBtn').html('Get Stocks')
      $('#submitBtn').removeClass('btn-danger').addClass('btn-primary')
    }, 4000)

  } else {

    $('#submitBtn').removeClass('loading').html('<i class="icon-ok"></i> Done')
    scraperwiki.tool.redirect("/dataset/" + scraperwiki.box)

  }
}

var getSymbols = function() {
  $(this).attr('disabled', true)
  $(this).addClass('loading').html('Getting symbols&hellip;')
  var command = 'python tool/scrape_symbols.py'
  scraperwiki.exec(command, getSymbolsSuccess)
}

var getSymbolsSuccess = function(data) {
  $('#symbolBtn').attr('disabled', false)

  if (data.indexOf('File "tool/scrape_symbols.py"') != -1) {

    scraperwiki.alert('Error in scrape_symbols.py', data, true)
    $('#symbolBtn').removeClass('loading').html('<i class="icon-remove"></i> Error')
    $('#symbolBtn').removeClass('btn-default').addClass('btn-danger')

    setTimeout(function() {
      $('#symbolBtn').html('Get list of symbols')
      $('#symbolBtn').removeClass('btn-danger').addClass('btn-default')
    }, 4000)

  } else {

    window.location.replace('ticker_info.csv')
    $('#symbolBtn').removeClass('loading').addClass('btn-default')
    $('#symbolBtn').html('Get list of symbols')

  }
}

$(function() {
  $('#stocks_input').load('tickers.txt', function() {
    $('#stocks_input').attr('placeholder', "TWTR,FB").focus()
  })
  $('#submitBtn').on('click', runScraper)
  $('#symbolBtn').on('click', getSymbols)
})

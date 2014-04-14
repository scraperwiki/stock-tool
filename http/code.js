var runScraper = function() {
  $(this).attr('disabled', true)
  $(this).addClass('loading').html('Scraping&hellip;')
  var stocks = $('#stocks_input').val()
  var escaped_stocks = scraperwiki.shellEscape(stocks)
  scraperwiki.exec('python tool/pandas_finance.py ' + escaped_stocks, getStocksSuccess)
}

var getStocksSuccess = function(data) {

    $('#submitBtn').attr('disabled', false)

  if (data.indexOf('File "tool/pandas_finance.py"') != -1) {

    scraperwiki.alert('Error in pandas_finance.py', data, true)
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

$(function() {
  $('#submitBtn').on('click', runScraper)
})

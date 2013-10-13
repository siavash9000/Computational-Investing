__author__ = 'siavash'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.DataAccess as dataAccess
import numpy as numpy

# Third Party Imports
import datetime as dateTime
import pandas as pandas

print "Pandas Version", pandas.__version__

def simulate (startDate, endDate, stocks, stocksDistribution):
    print(startDate, endDate, stocks,stocksDistribution)

def main():
    # Start and End date of the charts
    dateTimeStart = dateTime.datetime(2006, 1, 1)
    dateTimeEnd = dateTime.datetime(2010, 12, 31)

    # We need closing prices so the timestamp should be hours=16.
    dateTimeToday = dateTime.timedelta(hours=16)

    listOfTradingDays = dateUtil.getNYSEdays(dateTimeStart, dateTimeEnd, dateTimeToday)

    # Keys to be read from the data, it is good to read everything in one go.
    listDataKeys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    listStocks = ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
    dataFrame = dataAccess.DataAccess('Yahoo').get_data(listOfTradingDays, listStocks, listDataKeys)
    dictionaryStockData = dict(zip(listDataKeys, dataFrame))

    # Filling the data for NAN
    for s_key in listDataKeys:
        dictionaryStockData[s_key] = dictionaryStockData[s_key].fillna(method='ffill')
        dictionaryStockData[s_key] = dictionaryStockData[s_key].fillna(method='bfill')
        dictionaryStockData[s_key] = dictionaryStockData[s_key].fillna(1.0)

    # Getting the numpy ndarray of close prices.
    na_price = dictionaryStockData['close'].values
    simulate(dateTimeStart,dateTimeEnd,listStocks,[0.2,0.3,0.4,0.1])

if __name__ == '__main__':
    main()


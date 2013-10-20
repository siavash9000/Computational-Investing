__author__ = 'siavash'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.DataAccess as dataAccess
import numpy as numpy

# Third Party Imports
import datetime as dateTime
import pandas as pandas
import QSTK.qstkutil.tsutil as tsutil
print "Pandas Version", pandas.__version__

def findOptimalWeightVector(startDate, endDate, stocks):
    maxSharpeRatio = 0;
    maxWeightVector = [0.0,0.0,0.0,0.0]

    for x1 in range(0,11):
        for x2 in range(0,11):
            for x3 in range(0,11):
                for x4 in range(0,11):
                    weightVector = [x1*0.1,x2*0.1,x3*0.1,x4*0.1]
                    if isLegalWeightVector(weightVector):
                        sharpeRatio,standardDeviation, averageDailyReturn,cumulativeReturn =  simulate(startDate,endDate,stocks,weightVector)
                        if (sharpeRatio>maxSharpeRatio):
                            maxSharpeRatio = sharpeRatio
                            maxWeightVector = weightVector
                            print "sharpe,",sharpeRatio,"weightvector",weightVector

    sharpeRatio,standardDeviation, averageDailyReturn,cumulativeReturn =  simulate(startDate,endDate,stocks,maxWeightVector)
    print "weightVector",maxWeightVector
    print "sharpeRatio",sharpeRatio
    print "standardDeviation",standardDeviation
    print "averageDailyReturn",averageDailyReturn
    print "cumulativeReturn",cumulativeReturn

def isLegalWeightVector(weightVector):
    if numpy.sum(weightVector) == 1.0:
        return True
    else:
        return False

def simulate (startDate, endDate, stocks, stocksDistribution):
    stockDataDictionary=getStockDataAsDictionary(startDate,endDate,stocks)
    closePrices = stockDataDictionary['close'].values
    closePrices = closePrices
    normalizedPrices = closePrices.copy()
    normalizedPrices = normalizedPrices / normalizedPrices[0,:]
    dailyReturns = normalizedPrices.copy()
    tsutil.returnize0(dailyReturns)
    sumDailyreturns = numpy.sum(dailyReturns*stocksDistribution,axis=1)
    standardDeviation = numpy.std(sumDailyreturns)
    averageDailyReturn = numpy.average(sumDailyreturns)
    sharpeRatio = tsutil.get_sharpe_ratio(sumDailyreturns)
    # Estimate portfolio returns
    cumulativeReturn = numpy.prod(sumDailyreturns+1)
    return sharpeRatio,standardDeviation,averageDailyReturn,cumulativeReturn

def getStockDataAsDictionary(startDate, endDate, stocks):
    # We need closing prices so the timestamp should be hours=16.
    dateTimeToday = dateTime.timedelta(hours=16)
    listOfTradingDays = dateUtil.getNYSEdays(startDate, endDate, dateTimeToday)

    # Keys to be read from the data, it is good to read everything in one go.
    listDataKeys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    dataFrame = dataAccess.DataAccess('Yahoo', cachestalltime=1).get_data(listOfTradingDays, stocks, listDataKeys)
    dictionaryStockData = dict(zip(listDataKeys, dataFrame))

    # Getting the numpy ndarray of close prices.
    return dictionaryStockData

def main():
    # Start and End date of the charts
    dateTimeStart = dateTime.datetime(2011, 1, 1)
    dateTimeEnd = dateTime.datetime(2011, 12, 31)
    print("StartDate:",dateTimeStart)
    print("EndDate",dateTimeEnd)
    listStocks =  ['BRCM', 'TXN', 'AMD', 'ADI']
    print("Symbols:",listStocks)
    findOptimalWeightVector(dateTimeStart,dateTimeEnd,listStocks)

if __name__ == '__main__':
    main()


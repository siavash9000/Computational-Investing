__author__ = 'siavash'

__author__ = 'siavash'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.DataAccess as dataAccess
import numpy as numpy
import csv
import datetime
import sys

# Third Party Imports
import datetime
import pandas
import QSTK.qstkutil.tsutil as tsutil
print "Pandas Version", pandas.__version__


def simulate(values):
    values = values
    normalizedvalues = values
    normalizedvalues = normalizedvalues[:] / normalizedvalues[0]
    dailyreturns = normalizedvalues.copy()
    tsutil.returnize0(dailyreturns)
    standarddeviation = numpy.std(dailyreturns)
    averagedailyreturn = numpy.average(dailyreturns)
    sharperatio = tsutil.get_sharpe_ratio(dailyreturns)
    # Estimate portfolio returns>
    cumulativereturn = numpy.prod(dailyreturns+1)
    return sharperatio,standarddeviation,averagedailyreturn,cumulativereturn


def get_stockdata(startDate, endDate, stocks):
    # We need closing prices so the timestamp should be hours=16.
    datetimetoday = datetime.timedelta(hours=16)
    tradingdays = dateUtil.getNYSEdays(startDate, endDate, datetimetoday)

    # Keys to be read from the data, it is good to read everything in one go.
    datakeys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    dataframe = dataAccess.DataAccess('Yahoo', cachestalltime=1).get_data(tradingdays, stocks, datakeys)
    dictionaryStockData = dict(zip(datakeys, dataframe))

    # Getting the numpy ndarray of close prices.
    return dictionaryStockData


def extract_dates_and_values(filename):
    print "Start reading file ", filename
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    dates = []
    values = []
    for row in reader:
        dates.append(datetime.datetime(int(row[0]), int(row[1]), int(row[2]), 16))
        values.append(float(row[3]))
    valuesnumpy_array = numpy.array(values)
    return dates, valuesnumpy_array


def main():
    # Start and End date of the charts
    values_filename = sys.argv[1]
    benchmark_symbol = sys.argv[2]
    dates, values = extract_dates_and_values(values_filename)
    print simulate(values)
    import datetime
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.cbook as cbook

    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    # load a numpy record array from yahoo csv data with fields date,
    # open, close, volume, adj_close from the mpl-data/example directory.
    # The record array stores python datetime.date as an object array in
    # the date column

    fig, ax = plt.subplots()
    ax.plot(dates, values)


    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = datetime.date(dates[0].year, 1, 1)
    datemax = datetime.date(dates[-1].year+1, 1, 1)
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    def price(x): return '$%1.2f'%x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = price
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    plt.show()
if __name__ == '__main__':
    main()


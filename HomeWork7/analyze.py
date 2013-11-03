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
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
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
    return sharperatio,standarddeviation,averagedailyreturn,cumulativereturn, dailyreturns


def extract_dates_and_values(filename):
    print "Start reading file ", filename
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    dates = []
    values = []
    for row in reader:
        dates.append(datetime.datetime(int(row[0]), int(row[1]), int(row[2]), 16))
        values.append(float(row[3]))
    valuesnumpy_array = numpy.array(values)
    print dates[0],dates[-1]
    return dates, valuesnumpy_array


def _read_bench(symbol, timestamps):

    dataobj = dataAccess.DataAccess('Yahoo')
    close = dataobj.get_data(timestamps, [symbol], "close", verbose=True)
    close = close.fillna(method='ffill')
    close = close.fillna(method='bfill')
    return close[symbol]


def analyzebenchmark(benchmark_symbol, dates):
    stockdata = _read_bench(benchmark_symbol, dates)
    #print stockdata
    sharperatio, standarddeviation, averagedailyreturn, cumulativereturn, dailyreturns = simulate(stockdata)
    print benchmark_symbol, " analysis"
    print "sharperatio:", sharperatio
    print "standarddeviation:", standarddeviation
    print "averagedailyreturn", averagedailyreturn
    print "cumulativereturn", cumulativereturn
    return dailyreturns+1


def draw_timeseries(benchmark_symbol, dates, values, benchmark_values):
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    fig, ax = plt.subplots()
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    datemin = datetime.date(dates[0].year, 1, 1)
    datemax = datetime.date(dates[-1].year + 1, 1, 1)
    ax.set_xlim(datemin, datemax)
    ax.plot(dates, values)
    ax.plot(dates,benchmark_values)
    # format the coords message box
    def price(x): return '$%1.2f' % x

    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = price
    ax.grid(True)
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    plt.title("Your portfolio returns, benchmark "+benchmark_symbol)
    plt.show()



def main():
    # Start and End date of the charts
    values_filename = sys.argv[1]
    benchmark_symbol = sys.argv[2]
    dates, values = extract_dates_and_values(values_filename)

    sharperatio,standarddeviation,averagedailyreturn,cumulativereturn, dailyreturns =simulate(values)
    print "fund analysis"
    print "sharperatio:",sharperatio
    print "standarddeviation:",standarddeviation
    print "averagedailyreturn",averagedailyreturn
    print "cumulativereturn", cumulativereturn
    dailyreturns_benchmark = analyzebenchmark(benchmark_symbol, dates)
    dailyreturns_benchmark[0] = dailyreturns_benchmark[0]*values[0]
    benchmark_returns = dailyreturns_benchmark.cumprod()
    draw_timeseries(benchmark_symbol, dates, values, benchmark_returns)
if __name__ == '__main__':
    main()


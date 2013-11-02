__author__ = 'siavash'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.DataAccess as dataAccess
import numpy as numpy

# Third Party Imports
import datetime as dateTime
import pandas as pandas
import QSTK.qstkutil.tsutil as tsutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
print "Pandas Version", pandas.__version__


def readprices(symbol, timestamps):
    dataobj = dataAccess.DataAccess('Yahoo')
    close = dataobj.get_data(timestamps, [symbol], "close", verbose=True)
    close = close.fillna(method='ffill')
    close = close.fillna(method='bfill')
    return close[symbol]


def draw_bollingerband(dates,prices,rollingmean,upperband,lowerband):
    years    = mdates.YearLocator()   # every year
    months   = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots()

    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = datetime.date(dates[0].year, 1, 1)
    datemax = datetime.date(dates[-1].year+1, 1, 1)
    ax.set_xlim(datemin, datemax)
    ax.plot(dates, prices)
    ax.plot(dates, rollingmean)
    ax.plot(dates,upperband)
    ax.plot(dates,lowerband)
    # format the coords message box
    def price(x): return '$%1.2f'%x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = prices
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    plt.show()

def main():
    # Start and End date of the charts
    startdate = dateTime.datetime(2009, 1, 1)
    enddate = dateTime.datetime(2011, 12, 31)
    todaydate = dateTime.timedelta(hours=16)
    timestamps = dateUtil.getNYSEdays(startdate, enddate, todaydate)
    print("Startdate:",startdate)
    print("Enddate",enddate)
    symbol = 'MSFT'
    print("Symbol:",symbol)
    prices = readprices(symbol,timestamps)
    rollingmean = pandas.rolling_mean(prices,20)
    rollingstd = pandas.rolling_std(prices,20)
    upperband = rollingmean + rollingstd
    lowerband = rollingmean - rollingstd

    bollinger_value = (prices - rollingmean) / rollingstd
    for i in range(0,len(bollinger_value)):
        print timestamps[i],bollinger_value[i]
    draw_bollingerband(timestamps,prices,rollingmean,upperband,lowerband)

if __name__ == '__main__':
    main()


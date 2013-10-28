__author__ = 'siavash'

# QSTK Imports
import QSTK.qstkutil.qsdateutil as dateUtil
import QSTK.qstkutil.DataAccess as dataAccess
import numpy as numpy

# Third Party Imports
import datetime
import pandas
import copy
import QSTK.qstkutil.tsutil as tsutil
import csv
import sys

print "Pandas Version", pandas.__version__


def extract_dates_and_symbols(filename):
    print "Start reading file ", filename
    reader = csv.reader(open(filename, 'rU'), delimiter=',')
    dates = []
    symbols = []
    orders = []
    for row in reader:
        date = datetime.datetime(int(row[0]), int(row[1]), int(row[2]), 16)
        dates.append(date)
        symbol = row[3]
        symbols.append(symbol)
        amount = row[5]
        if row[4] == 'Buy':
            orders.append([date, symbol, (int(amount))])
        else:
            orders.append([date, symbol, (-int(amount))])

    symbols = list(set(symbols))
    return dates, symbols, orders


def get_stockdata(startdate, enddate, stocks):
    # We need closing prices so the timestamp should be hours=16.
    datetime_today = datetime.timedelta(hours=16)
    tradingdays = dateUtil.getNYSEdays(startdate, enddate, datetime_today)

    # Keys to be read from the data, it is good to read everything in one go.
    list_datakeys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    dataframe = dataAccess.DataAccess('Yahoo', cachestalltime=1).get_data(tradingdays, stocks, list_datakeys)
    stockdata = dict(zip(list_datakeys, dataframe))

    # Getting the numpy ndarray of close prices.
    return stockdata, tradingdays


def create_tradematrix(stockdata, tradingdays, symbols):
    tradematrix = pandas.DataFrame(stockdata, index=tradingdays, columns=symbols)
    #init tradematrix with zeros
    for symbol in symbols:
       tradematrix[:][symbol] = 0.0
    return tradematrix


def addorders(tradematrix, dates, symbols, orders):
    for order in orders:
        tradematrix[order[0]:tradematrix.index[-1]][order[1]] += order[2]


def create_cashseries(tradingdays, startcash, orders, prices):
    cash = pandas.Series(0, index=tradingdays)
    cash[0:-1] = float(startcash)
    for day in tradingdays:
       for order in orders:
            if order[0] == day:
                cash[day:cash.index[-1]] = cash[day:day] - prices[day:day][order[1]]*order[2]

    return cash


def main():
    startcash = float(sys.argv[1])
    order_filename = sys.argv[2]
    outputfilename = sys.argv[3]
    dates, symbols, orders = extract_dates_and_symbols(order_filename)
    starttime = min(dates)
    endtime = max(dates) + datetime.timedelta(days=1)
    stockdata, tradingdays = get_stockdata(starttime, endtime, symbols)
    prices = stockdata['close']
    prices = prices.fillna(method='ffill')
    prices = prices.fillna(method='bfill')

    tradematrix = create_tradematrix(stockdata, tradingdays, symbols)
    addorders(tradematrix, dates, symbols, orders)
    cash = create_cashseries(tradingdays, startcash, orders, prices)
    prices['_CASH'] = 1.0
    tradematrix['_CASH'] = cash
    tradematrix = tradematrix*prices
    tradematrix['_VALUE'] = 0.0
    writer = csv.writer(open(outputfilename,'wb'),delimiter=',')
    for day in tradematrix.index:
        for symbol in symbols:
            tradematrix[day:day]['_VALUE'] += tradematrix[day:day][symbol]
        tradematrix[day:day]['_VALUE'] = tradematrix[day:day]['_VALUE'] + tradematrix[day:day]['_CASH']
        print(tradematrix[day:day]['_VALUE'].to_string())
        row = day , int(tradematrix[day:day]['_VALUE'])
        writer.writerow(row)

if __name__ == '__main__':
    main()


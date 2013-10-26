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
        symbols.append(row[3])
        if row[4] == 'Buy':
            orders.append([date, row[3], (int(row[5]))])
        else:
            orders.append([date, row[3], (-int(row[5]))])

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


def create_tradetmatrix(dates, symbols):
    starttime = min(dates)
    endtime = max(dates) + datetime.timedelta(days=1)
    symbols_without_duplicates = copy.deepcopy(symbols)
    symbols_without_duplicates = list(set(symbols_without_duplicates))
    stockdata, tradingdays = get_stockdata(starttime, endtime, symbols_without_duplicates)
    tradematrix = pandas.DataFrame(stockdata, index=tradingdays, columns=symbols_without_duplicates)
    #init tradematrix with zeros
    for day in tradingdays:
        for symbol in symbols_without_duplicates:
            tradematrix[:day][symbol] = 0
    return tradematrix


def addorders(tradematrix, dates, symbols, orders):
    for order in orders:
        tradematrix[order[0]:order[0]][order[1]] = order[2]


def main():
    dates, symbols, orders = extract_dates_and_symbols("orders.csv")
    tradematrix = create_tradetmatrix(dates, symbols)
    addorders(tradematrix, dates, symbols, orders)
    print tradematrix


if __name__ == '__main__':
    main()


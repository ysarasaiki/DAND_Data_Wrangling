# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

DATADIR = ''
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    # Read headers into a list
    headers = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols - 1)]
    # Read datetimes into a list
    dates = [xlrd.xldate_as_tuple(sheet.cell_value(row_index,0),0) for row_index in range(1,sheet.nrows)]

    for data_col in range(1,sheet.ncols - 1):
        max_value = 0
        index = 0
        for data_row in range(1,sheet.nrows):
            if sheet.cell_value(data_row, data_col) > max_value:
                max_value = sheet.cell_value(data_row, data_col)
                index = data_row
        key = headers[data_col]
        max_datetime = dates[index - 1]

        newlist = [max_datetime[i] for i in xrange(4)]
        newlist.append(max_value)
        newlist.insert(0,key)
        data.append(newlist)
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'wb') as f:
        fieldnames = ['Station','Year', 'Month', 'Day', 'Hour', 'Max Load']
        w = csv.writer(f,delimiter = '|')
        w.writerow(fieldnames)
        w.writerows(data)

save_file(parse_file(os.path.join(DATADIR, datafile)),outfile)

'''
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
'''

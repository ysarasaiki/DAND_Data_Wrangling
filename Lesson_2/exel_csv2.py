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
outfile = "2013_Max_Loads_2.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = {}

    # Loop through all station columns
    for col_index in range(1, sheet.ncols):
        # first row is the station
        station = sheet.cell_value(0,col_index)
        values = sheet.col_values(col_index, start_rowx = 1, end_rowx = None) # returns list of values

        max_value = max(values)
        max_value_row = values.index(max_value) + 1
        max_value_time = sheet.cell_value(max_value_row, 0)
        max_real_time = xlrd.xldate_as_tuple(max_value_time, 0)

        data[station] = {"maxval" : max_value, "maxtime": max_real_time}
    #print data
    return data

# output of:
# { STATION:
#        { maxval : int
#          maxtime : tuple
#        }
#   }


parse_file(os.path.join(DATADIR, datafile))

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'wb') as f:
        w = csv.writer(f,delimiter = '|')
        w.writerow(['Station','Year', 'Month', 'Day', 'Hour', 'Max Load'])
        for stations in data:
            y, m, d, h, _, _ = data[stations]["maxtime"]
            w.writerow([stations, y, m, d, h, data[stations]["maxval"]])
            #w.writerow(fieldnames)
        #w.writerows(data)

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

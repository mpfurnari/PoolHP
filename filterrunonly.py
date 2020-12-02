from os import truncate
import sys 
import csv
import datetime
from datetime import timedelta

import numpy as np
arr = np.empty(36, dtype=object) 
idx = 0;

minkw = 200
maxkw = 1200
kwcol = 2

skiprows = 3

filename = sys.argv[1]

with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    
        skiprows = skiprows -1
        if (skiprows <= 0) :
            if (float(row[kwcol]) > minkw):
                if (float(row[kwcol]) < maxkw):
                       rowstr = str(row)[1:-1]
                       rowstr = rowstr.replace("'", "")
                       print(rowstr)
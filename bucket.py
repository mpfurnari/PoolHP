from os import truncate
import sys 
import csv
import datetime
from datetime import timedelta

import numpy as np
arr = np.empty(36, dtype=object) 
idx = 0;

pooltempcol = 4


filename = sys.argv[1]
prevbucket = -1
prevsec = 0

with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rowtime = row[0]
        try:
             date_time_obj = datetime.datetime.strptime(rowtime[:26], '%Y-%m-%d %H:%M:%S.%f')
             newbucket = int(date_time_obj.minute/5 )
             cont = True
        except:
            cont = False
        if (cont):    
         if (prevbucket != newbucket):
           duration_in_s = date_time_obj.timestamp() - prevsec;
           hours = divmod(duration_in_s, 3600)[0]  
           minutes = divmod(duration_in_s, 60)[0]    
#           print('Date:', date_time_obj.date(), " 5min bucket", int(date_time_obj.minute/5 ), " min Diff = ", duration_in_s/60)
           arr[idx] = row
           currsec = date_time_obj.timestamp();

           idxnext = (idx+1) % 36;
           if (arr[idxnext] != None):
               try: 
                   arrprevsec = datetime.datetime.strptime(arr[idxnext][0][:26], '%Y-%m-%d %H:%M:%S.%f').timestamp()
               except:
                   arrprevsec = 0
               if (arrprevsec != 0): 
                  elapsed_min = (currsec - arrprevsec)/60
                  queued_pool_temp = float(arr[idxnext][pooltempcol])
                  latest_pool_temp = float(arr[idx][pooltempcol])
                  delta_temp = latest_pool_temp - queued_pool_temp
                  delta_temp_per_hour = (latest_pool_temp-queued_pool_temp)/(elapsed_min/60)
                  rowstr = str(arr[idxnext])[1:-1] 
                  rowstr = rowstr.replace("'", "")
                  print (rowstr, ", ", elapsed_min, ", ", delta_temp, ", ",delta_temp_per_hour)

           idx = idxnext    
           prevbucket = newbucket
           prevsec = currsec

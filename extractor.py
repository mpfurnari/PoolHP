#!/usr/bin/python3

import psycopg2
import numpy as np
import math
import credlib


print ('starting')
con = psycopg2.connect(dbname=credlib.dbname, host=credlib.host, user=credlib.user, password=credlib.password)
cur = con.cursor()

cur.execute("select entity_id, last_changed, state from states where entity_id='sensor.hppower' OR entity_id='sensor.poolheatedtemp' OR entity_id='sensor.poolreturntemp' OR entity_id='sensor.dark_sky_temperature' OR entity_id='sensor.dark_sky_uv_index' ORDER BY last_changed")

collect = False
poolheatedtemp = np.nan
poolreturntemp = np.nan
uv_index = np.nan
dark_sky_temperture = np.nan
hppower = np.nan
last_changed_last = ""


# Print Header
print("last_changed,hdpower, poolheatedtemp, poolreturntemp, dark_sky_temperture, efficiency, dark_sky_uv_index")

# Collect/Print data
for entity, last_changed, value in cur:

    if (value == "unavailable") or (value == "unknown"):
        state = np.nan
    else:
        state = float(value)

    # Should we be collecting
    if entity == 'sensor.hppower':
        if state > 500:
            collect=True
        else:
            collect=False

    if entity == 'sensor.dark_sky_uv_index':
        uv_index = state
        last_changed_last = last_changed
    elif entity == 'sensor.poolheatedtemp':
        poolheatedtemp = state
        last_changed_last = last_changed
    elif entity == 'sensor.poolreturntemp':
        poolreturntemp = state
        last_changed_last = last_changed
    elif entity == 'sensor.dark_sky_temperature':
        dark_sky_temperture = state
        last_changed_last = last_changed
    elif entity == 'sensor.hppower':
        hdpower = state
        last_changed_last = last_changed
    else:
        raise ValueError('Unknown entity found')

    if collect is True:
        if not(math.isnan(hdpower)) and not(math.isnan(poolheatedtemp)) and not(math.isnan(poolreturntemp)) and not(math.isnan(dark_sky_temperture)):
            efficiency = (poolheatedtemp - poolreturntemp) * 10000 / hdpower
            if (efficiency != 0):
               print(str(last_changed_last) + ", " + str(hdpower) + ", " + str(poolheatedtemp) + ", " + str(poolreturntemp) + ", " + str(dark_sky_temperture) + ", " + str(efficiency) + ", " + str(uv_index))

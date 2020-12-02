#!/usr/bin/python3

import psycopg2
import numpy as np
import math
import credlib


print ('starting')
con = psycopg2.connect(dbname=credlib.dbname, host=credlib.host, user=credlib.user, password=credlib.password)
cur = con.cursor()

execStr = ("select entity_id, last_changed, state from states where " +
             "entity_id='sensor.hppower' OR " +
             "entity_id='sensor.poolheatedtemp' OR  " +
             "entity_id='sensor.pumppower' OR " +
             "entity_id='sensor.dark_sky_humidity' OR " +
             "entity_id='sensor.poolreturntemp' OR " +
             "entity_id='sensor.dark_sky_temperature' OR " +
             "entity_id='sensor.dark_sky_uv_index' " +
             "ORDER BY last_changed")

cur.execute(execStr)

collect = False
poolheatedtemp = np.nan
poolreturntemp = np.nan
uv_index = np.nan
outsidetemperture = np.nan
outsidehumidity = np.nan
pumppower = np.nan
hppower = np.nan

last_changed_last = ""


# Print Header
print("last_changed,hppower, pumppower, poolheatedtemp, poolreturntemp, outsidetemperture, outsidehumidity, uvindex,  efficiency")

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

    collect = True # now collecting everything.
            

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
        outsidetemperture = state
        last_changed_last = last_changed
    elif entity == 'sensor.hppower':
        hppower = state
        last_changed_last = last_changed
    elif entity == 'sensor.pumppower':
        pumppower = state
        last_changed_last = last_changed
    elif entity == 'sensor.dark_sky_humidity':
        outsidehumidity = state
        last_changed_last = last_changed
    else:
        raise ValueError('Unknown entity found')

    if collect is True:
        if (not(math.isnan(hppower)) and
           not(math.isnan(pumppower)) and 
           not(math.isnan(poolheatedtemp)) and 
           not(math.isnan(poolreturntemp)) and 
           not(math.isnan(outsidetemperture)) and 
           not(math.isnan(outsidehumidity)) and 
           not(math.isnan(uv_index))):

            if (hppower != 0 ):
               efficiency = (poolheatedtemp - poolreturntemp) * 10000 / hppower
            else:
                efficiency = np.infty
            print(str(last_changed_last) + ", " + 
                     str(hppower) + ", " + 
                     str(pumppower) + ", " + 
                     str(poolheatedtemp) + ", " + 
                     str(poolreturntemp) + ", " + 
                     str(outsidetemperture) + ", " + 
                     str(outsidehumidity) + ", " + 
                     str(uv_index) + ", " + 
                     str(efficiency))

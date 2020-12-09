import numpy as np
import pandas as pd
from pysolar import solar

lat = 38.291969
lon = 21.788156

def read_raw(fname):
    df = pd.read_csv(fname, 
                      names= ['t','SV','GHI','DHI'], # sv: sun visibility (seconds)
                      parse_dates=True, index_col='t')
    df = df.tz_localize('UTC')
    # selecting less data to reduce calc time, solar noon 10:16 to 10:47 UTC 
    df = df.between_time("07:00", "14:00")
    return df

def calc_solar_angles(df):
    sol_index = df.index.to_pydatetime()
    zenith = [90 - solar.get_altitude_fast(lat,lon, t) for t in sol_index]
    # .item() is used because get_azimuth_fast() returns 0-d ndArray
    azimuth = [solar.get_azimuth_fast(lat,lon, t).item() for t in sol_index] 
    df = df.assign(zen = zenith)
    df = df.assign(az = azimuth)
    return df

sol = read_raw('raw/solar_2016.txt')    
sol = calc_solar_angles(sol)
sol['DNI']= (sol["GHI"] - sol["DHI"])/np.cos(np.deg2rad(sol['zen']))
sol.to_csv("solar.csv")
# solar_noons = sol.loc[sol.groupby(sol.index.date)["zen"].idxmin()]

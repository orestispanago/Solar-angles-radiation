import pandas as pd
from pysolar import solar

lat = 38.291969
lon = 21.788156

def read_raw(fname):
    df = pd.read_csv(fname, 
                      names= ['t','sv','ghi','dhi'], # sv =sun visibility in seconds,
                      parse_dates=True, index_col='t')
    # solar noon 10:16 to  10:47 UTC) 
    df = df.tz_localize('UTC')
    df = df.between_time("07:00", "14:00")
    return df

def calc_solar_angles(df):
    sol_index = df.index.to_pydatetime()
    altitude = [solar.get_altitude_fast(lat,lon, t) for t in sol_index]
    # .item() is used because get_azimuth_fast() returns 0-d ndArray
    azimuth = [solar.get_azimuth_fast(lat,lon, t).item() for t in sol_index] 
    df = df.assign(alt = altitude)
    df = df.assign(az = azimuth)
    return df

sol = read_raw('raw/solar_2016.txt')    
sol = calc_solar_angles(sol)
sol.to_csv("sol.csv")
# large['dni']= np.where((large['zen'] < 89) & (large['ghi']>=large['dhi']), (large['ghi']-large['dhi'])/np.cos(np.deg2rad(large['zen'])),0)

# solar_noons = sol.loc[sol.groupby(sol.index.date)["alt"].idxmax()]

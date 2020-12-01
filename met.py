import pandas as pd
from pysolar import solar

lat = 38.291969
lon = 21.788156


sol_header = ['t','sv','ghi','dhi'] # sv =sun visibility in seconds

sol = pd.read_csv('raw/solar_2016.txt', names=sol_header,
                  parse_dates=True, index_col='t')

# solar noon is from 
# Nov 1st (DOY 305) 
# 12.16 (10.16 UTC) 
# to Aug 1st (DOY 213) 
# 13.39 (10:39 UTC)
# select between 06:30 to 14:30
sol = sol.tz_localize('UTC')
sol = sol.between_time("07:00", "14:00")
# sol[sol.isnull().any(axis=1)] # NaNs
# sol = sol.resample("1min").mean()

sol_index = sol.index.to_pydatetime()

alt = [solar.get_altitude_fast(lat,lon, t) for t in sol_index]
# .item() is used because get_azimuth_fast() returns 0-d ndArray
az = [solar.get_azimuth_fast(lat,lon, t).item() for t in sol_index] 


sol = sol.assign(alt = alt)
sol = sol.assign(az = az)
# large['dni']= np.where((large['zen'] < 89) & (large['ghi']>=large['dhi']), (large['ghi']-large['dhi'])/np.cos(np.deg2rad(large['zen'])),0)

solar_noons = sol.loc[sol.groupby(sol.index.date)["alt"].idxmax()]

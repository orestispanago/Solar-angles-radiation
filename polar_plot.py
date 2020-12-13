import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()


df = pd.read_csv("solar.csv", parse_dates=True, index_col='t')


df["az"].plot.hist()
df["zen"].plot.hist()


df[['az', 'zen']] = df[['az', 'zen']].apply(np.radians)

rbins = np.linspace(0, df["zen"].max(), 50)
abins = np.linspace(0, 2*np.pi, 60)

# The weighted histogram is the sum of all the weights for each given bin
# Divide the two, to get the average
# see https://stackoverflow.com/questions/63758336/how-to-create-a-polar-plot-with-azimuth-zenith-and-a-averaged-weight-value
hist, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins), weights=df["GHI"])
hist2, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins))
# hist, _, _ = np.histogram2d(df["az"], df["zen"], density=True, weights=df["GHI"], bins=(abins, rbins))
# hist[hist == 0] = np.nan # or use np.nan
avg_hist = hist / hist2
A, R = np.meshgrid(abins, rbins)

fig, ax = plt.subplots(subplot_kw=dict(projection="polar"), figsize=(7, 7))

pc = ax.pcolormesh(A, R, hist2.T, cmap="jet")
ax.set_theta_zero_location("N")
fig.colorbar(pc)
plt.grid()
plt.show()

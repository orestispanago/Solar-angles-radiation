import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import mkdir_if_not_exists
import os

quantity = "GHI"
params = {
          'font.size': 16,
          'savefig.format': 'png',
           'savefig.dpi': 200.0,
          }
plt.rcParams.update(params)


df = pd.read_csv("raw/solar_all.csv", parse_dates=True, index_col='t')
# df = df.loc[(df["az"]>90) & (df["az"]<270)]
df = df.loc[(df["zen"]<90) & (df["DNI"]>0)]

df[["az","zen"]].plot.hist(alpha=0.5, bins=30)


df[['az', 'zen']] = df[['az', 'zen']].apply(np.radians)


rbins = np.linspace(0, df["zen"].max(), 30)
abins = np.linspace(0, 2*np.pi, 60)

# The weighted histogram is the sum of all the weights for each given bin
# Divide the two, to get the average
# see https://stackoverflow.com/questions/63758336/how-to-create-a-polar-plot-with-azimuth-zenith-and-a-averaged-weight-value
hist, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins))
hist_weights, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins), weights=df[quantity])
hist_weights_kwh, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins), weights=df[quantity]/60000)
# hist, _, _ = np.histogram2d(df["az"], df["zen"], density=True, weights=df["GHI"], bins=(abins, rbins))
avg_hist = hist_weights / hist
A, R = np.meshgrid(abins, rbins)


def plot_polar_heatmap(histogram, cbar_label="", pic_path=None):
    histogram[histogram == 0] = np.nan # or use np.nan
    fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))
    pc = ax.pcolormesh(A, R, histogram.T, cmap="jet")
    ax.set_yticklabels([])
    ax.set_theta_zero_location("N")
    cbar = fig.colorbar(pc,pad = 0.15)
    cbar.ax.set_title(cbar_label)
    ax.tick_params(pad=14)
    plt.grid()
    if pic_path:
        mkdir_if_not_exists(os.path.dirname(pic_path))
        plt.savefig(pic_path)
    plt.show()

plot_polar_heatmap(hist, cbar_label="count", pic_path=f"pics/{quantity}/count.png")
plot_polar_heatmap(hist_weights_kwh, cbar_label="$kWh$", pic_path=f"pics/{quantity}/kwh.png")
plot_polar_heatmap(avg_hist, cbar_label="$W \cdot m^{−2}$", pic_path=f"pics/{quantity}/avg_wm2.png")


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
params = {'figure.figsize': (14, 4),
          'axes.titlesize': 20,
          'axes.titleweight': 'bold',
          'axes.labelsize': 20,
          'axes.labelweight': 'bold',
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          'font.weight': 'bold',
          'font.size': 20,
          'legend.fontsize': 16,
          'savefig.format': 'png',
          # 'savefig.dpi': 300.0,
          # 'figure.constrained_layout.use': True,
          }
plt.rcParams.update(params)


df = pd.read_csv("solar_all.csv", parse_dates=True, index_col='t')
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
hist_weights, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins), weights=df["GHI"])
hist_weights_kwh, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins), weights=df["GHI"]/60000)
# hist, _, _ = np.histogram2d(df["az"], df["zen"], density=True, weights=df["GHI"], bins=(abins, rbins))
avg_hist = hist_weights / hist
A, R = np.meshgrid(abins, rbins)


def plot_polar_heatmap(histogram, cbar_label="", pic_path=None):
    histogram[histogram == 0] = np.nan # or use np.nan
    fig, ax = plt.subplots(subplot_kw=dict(projection="polar"), figsize=(9, 7))
    pc = ax.pcolormesh(A, R, histogram.T, cmap="jet")
    ax.set_yticklabels([])
    ax.set_theta_zero_location("N")
    fig.colorbar(pc,pad = 0.1,label=cbar_label)
    ax.tick_params(pad=20)
    plt.grid()
    if pic_path:
        plt.savefig(pic_path)
    plt.show()

plot_polar_heatmap(hist, cbar_label="count", pic_path="pics/GHI/count")
plot_polar_heatmap(hist_weights_kwh, cbar_label="$kWh$", pic_path="pics/GHI/kwh")
plot_polar_heatmap(avg_hist, cbar_label="$Wm^{−2}$", pic_path="pics/GHI/avg_wm2")


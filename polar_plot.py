import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()


df = pd.read_csv("solar_all.csv", parse_dates=True, index_col='t')
# df = df.loc[(df["az"]>90) & (df["az"]<270)]
df = df.loc[df["zen"]<90]

df[["az","zen"]].plot.hist(alpha=0.5, bins=30)


df[['az', 'zen']] = df[['az', 'zen']].apply(np.radians)


rbins = np.linspace(0, df["zen"].max(), 50)
abins = np.linspace(0, 2*np.pi, 60)

# The weighted histogram is the sum of all the weights for each given bin
# Divide the two, to get the average
# see https://stackoverflow.com/questions/63758336/how-to-create-a-polar-plot-with-azimuth-zenith-and-a-averaged-weight-value
hist, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins))
hist_weights, _, _ = np.histogram2d(df["az"], df["zen"], bins=(abins, rbins), weights=df["GHI"])
# hist, _, _ = np.histogram2d(df["az"], df["zen"], density=True, weights=df["GHI"], bins=(abins, rbins))
avg_hist = hist_weights / hist
A, R = np.meshgrid(abins, rbins)

def plot_polar_heatmap(histogram, cbar_label=""):
    histogram[histogram == 0] = np.nan # or use np.nan
    fig, ax = plt.subplots(subplot_kw=dict(projection="polar"), figsize=(7, 7))
    pc = ax.pcolormesh(A, R, histogram.T, cmap="jet")
    ax.set_yticklabels([])
    ax.set_theta_zero_location("N")
    fig.colorbar(pc,pad = 0.1,label=cbar_label)
    plt.grid()
    plt.show()

plot_polar_heatmap(avg_hist)
plot_polar_heatmap(hist)
plot_polar_heatmap(hist_weights)

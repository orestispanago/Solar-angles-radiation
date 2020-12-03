import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_calendar_heatmap(dfin, col, freq="1min", units="", 
                          folder="calendar-heatmaps"):
    df = dfin.resample(freq).mean().dropna()
    df["Time, UTC"] = df.index.time
    df["Date"] = df.index.date
    df.reset_index(inplace=True)
    df = df.pivot("Time, UTC","Date", col)
    fig, ax = plt.subplots(figsize=(25,6))
    cbar_label = col + units
    ax = sns.heatmap(df, cmap="jet",cbar_kws={'label': cbar_label})
    plt.tight_layout()
    plt.savefig(f"{folder}/{col}.png")
    plt.show()

df = pd.read_csv("solar.csv", index_col="t", parse_dates=True)
plot_calendar_heatmap(df, "DNI", units=" ($\\frac{W}{m^2}$)")

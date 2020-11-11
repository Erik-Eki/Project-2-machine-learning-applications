import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from scipy.stats import zscore
import numpy as np
import pandas as pd

def find_outliers(df):
    # Check for missing values
    missing_count = df.isnull().sum()
    print("Number of missing variables in table\n", missing_count)

    # Check for unique values in columns
    print(f"{'-'*30}\nUnique values in columns\n")
    print("uniques in x",len(df['x'].unique()))
    print("uniques in y",len(df['y'].unique()))
    print("uniques in z",len(df['z'].unique()))
    print("uniques in q",len(df['q'].unique()))


    print(f"{'-'*30}\nChecking z and q columns\n")
    print("uniques in z",df['z'].unique())
    print("uniques in q",df['q'].unique())


    # Checking how many different nodes
    amount_nodes = len(df["node_id"].unique())
    print(f"{'-'*30}\nNumber of nodes: {amount_nodes}")

    # Only use the x and y columns
    df1 = df[["x","y"]]

    z_scores = zscore(df1)
    abs_z_scores = np.abs(z_scores)
    
    # Remove rows that have outliers in at least one column
    outliers = df1[(abs_z_scores <= 2.5).all(axis=1)]
    
    # Pidä vain ne rivit, jotka ovat +2.5 - -2.5 keskihajonnan sisällä.
    filtered_entries = (abs_z_scores <= 2.5).all(axis=1)
    df_clean = df[filtered_entries]
    

    # pd.concat lisää kaksi DataFrame-kehystä yhteen liittämällä ne peräkkäin.
    # jos on päällekkäisyyksiä, se kaapataan drop_duplicates:illa
    # drop_duplicates oletusarvoisesti jättää ensimmäisen havainnon ja poistaa kaikki muut havainnot.
    # Tässä tapauksessa haluamme, että jokainen kaksoiskappale poistetaan. Siksi keep = False -parametri
    potato = pd.concat([df1, outliers]).drop_duplicates(keep=False)

    print(f"{'-'*30}\nOutliers\n")
    print("Data with outliers: ", len(df))
    print("Ouliers removed:    ", len(df) - len(df_clean))
    print("Data after: ", len(df_clean))


    import matplotlib.pyplot as plt
    plt.gca().invert_yaxis()
    plt.plot(df_clean["x"], df_clean["y"], color="red", marker='o', linestyle='dashed', linewidth=0.2, markersize=3)
    plt.plot(potato["x"], potato["y"], color="blue", marker='x', linestyle='dashed', linewidth=0.2, markersize=3)
    plt.savefig("outliers-in-data.png")
    plt.show

    return df_clean

# Esim: draw_histogram(df2['x'], df2['y'], 20)
def draw_histogram(x, y, bin_num):
    plt.figure(figsize=(15,10))
    # mean of distribution
    mu = np.mean(x)
    mu2 = np.mean(y)
    print("x mean: ", mu)
    print("y mean: ", mu2)

    # standard deviation of distribution
    sigma = np.std(x)
    sigma2 = np.std(y)
    print("x std: ", sigma)
    print("y std: ", sigma2)

    # bins
    num_bins = bin_num

    # the histogram of the data
    n, bins, patches = plt.hist(x, num_bins, density=1, facecolor='orange', alpha=0.5, label='x')
    n2, bins2, patches2 = plt.hist(y, num_bins, density=1, facecolor='blue', alpha=0.5, label='y')

    # add a 'best fit' line
    y = norm.pdf(bins, mu, sigma)
    y2 = norm.pdf(bins2, mu2, sigma2)

    # This is what it norm.pdf does
    #y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    #y2 = ((1 / (np.sqrt(2 * np.pi) * sigma2)) * np.exp(-0.5 * (1 / sigma2 * (bins2 - mu2))**2))

    plt.plot(bins, y, 'r', alpha=0.8, label='x')
    plt.plot(bins2, y2, 'b', alpha=0.8, label='y')

    plt.title("Histogrammi lmao (bins %s)" % num_bins)
    plt.xlabel("Arvo")
    plt.ylabel("Tiheys")
    plt.legend()
    # Tweak spacing to prevent clipping of ylabel
    plt.tight_layout()
    plt.savefig('outliers-histogram.jpg')
    plt.show()
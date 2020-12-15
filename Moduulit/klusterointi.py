import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
def df_to_features(df):
    df["check"] = df["ajokerta"].shift(1)
    uniques = df["ajokerta"].unique()
    rivit = []
    asd = pd.DataFrame()
    for row in df.itertuples():
        if row.ajokerta != row.check:
            if len(df[df["ajokerta"] == row.ajokerta]["grid_id"].unique()) > 25:
                idt = np.array(df[df["ajokerta"] == row.ajokerta]["grid_id"].value_counts().keys().tolist()[:25])
                start_row = np.array(df[df["ajokerta"] == row.ajokerta].index[0])
                end_row = np.array(df[df["ajokerta"] == row.ajokerta].index[-1])
                rivit.append({"ajokerta":row.ajokerta, "node_id":row.node_id,"grid_id":row.grid_id, "time":row.timestamp, 
                              "kesto":row.kesto, "dayofweek":row.dayofweek, 
                              "current_hour":row.current_hour, "distance":row.distance,
                              "start":start_row, "end":end_row,
                              "0":idt[0], "1":idt[1], "2":idt[2], "3":idt[3],
                              "4":idt[4], "5":idt[5], "6":idt[6], "7":idt[7],
                              "8":idt[8], "9":idt[9], "10":idt[10], "11":idt[11],
                              "12":idt[12], "13":idt[13], "14":idt[14],"15":idt[15],
                              "16":idt[16], "17":idt[17], "18":idt[18], "19":idt[19],
                              "20":idt[20], "21":idt[21], "22":idt[22], "23":idt[23],"24":idt[24]})
    return pd.DataFrame(rivit)

def ideal_k(df):

    ideal_k = []
    for i in range(1,10,1):
        est_kmeans = KMeans(n_clusters=i)
        est_kmeans.fit(df)

        ideal_k.append([i,est_kmeans.inertia_])

    ideal_k = np.array(ideal_k)   
    plt.plot(ideal_k[:,0],ideal_k[:,1])
    plt.show()
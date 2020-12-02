import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.ensemble import IsolationForest


def isolation_forest(df, random_state, contamination, node):
    
    # x ja y arvot talteen
    x_temp = df.loc[df['node_id']==node][['x', 'y']]
        
    # Init minmaxscaler + fit+transform
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x_temp)
    
    # Normalisoidut arvot uuteen dataframeen
    xy_normalized = pd.DataFrame(x_scaled)
    xy_normalized = xy_normalized.rename(columns={0: 'x', 1: 'y'})
      
    # Isolationforest annetuin parametrein + fit
    clf = IsolationForest(max_samples=len(x_scaled),random_state=random_state, contamination=contamination) 
    clf.fit(xy_normalized)
    
    # Outlier detect
    if_scores = clf.decision_function(xy_normalized)
    if_anomalies=clf.predict(xy_normalized)
    if_anomalies=pd.Series(if_anomalies).replace([-1,1],[1,0])
    if_anomalies=xy_normalized[if_anomalies==1]
    
    outliers = x_temp.iloc[if_anomalies.index.values]
    print('Dataframe lenght before:', len(x_temp))
    
    # Drop outliers from df + reset index
    x_temp = x_temp.drop(x_temp.index[if_anomalies.index.values])
    
    # Grab that sweet timestamp
    df = df.loc[x_temp.index]
    df = df.reset_index(drop=True)
    
    print('Dataframe lenght after:', len(df))
    print('Total outliers detected:', len(if_anomalies))
    
    total_data = len(x_temp)
    total_missing = len(if_anomalies)
    percentage = (total_missing/total_data) * 100
    percentage_remain = (1 - (total_missing/total_data)) * 100
    print("Percent removed:   ",round(percentage, 2),'%')
    print("Percent remaining: ",round(percentage_remain, 2),'%')
    
    #Plot results
    #plt.gca().invert_yaxis()
    '''plt.scatter(df['x'],df['y'],edgecolor='black',s=15, label="Jääneet")
    plt.scatter(outliers['x'],outliers['y'],edgecolor='red',s=15, label="Poistetut")
    plt.ylabel("x")
    plt.ylabel("y", rotation='0')
    plt.legend()
    plt.show()'''
    
    return df, outliers

def plot_isolation_forest(df, outliers):
    """[Plottaa jokaisen kauppareissun peräkkäin]

     Args:
         df_reitit ([DataFrame]): [Sisältää erotellut kauppareitit]
         grid_size ([int]): [Gridin koko on määritelty tämän mukaan.]
     """
    node = df["node_id"].unique()
    node_len = max(df["node_id"].unique())

    #c = cm.flag(np.linspace(0, 1, ajot_len))
    plt.figure(figsize=(20,15))


    for i in range(ajot_len):
        plt.subplot((node_len/5)+1,4,i+1)
        plt.scatter(df['x'],df['y'],edgecolor='black',s=15, label="Jääneet")
        plt.scatter(outliers['x'],outliers['y'],edgecolor='red',s=15, label="Poistetut")
        plt.ylabel("x")
        plt.ylabel("y", rotation='0')
        plt.title(f"Node {i+1}")
        #plt.xlim(0, 40)
        #plt.ylim=(0, 40)
        #plt.axis('off')

    plt.show()
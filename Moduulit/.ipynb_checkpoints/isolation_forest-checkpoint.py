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
    
    outliers = x_temp.loc[if_anomalies.index.values]
    print('Dataframe lenght before:', len(x_temp))
    
    # Drop outliers from df + reset index
    x_temp = x_temp.drop(x_temp.index[if_anomalies.index.values])
    
    # Grab that sweet timestamp
    df = df.loc[x_temp.index]
    df = df.reset_index(drop=True)
    
    print('Dataframe lenght after:', len(df))
    print('Total outliers detected:', len(if_anomalies))
    
    #Plot results
    #plt.gca().invert_yaxis()
    plt.scatter(df['x'],df['y'],edgecolor='black',s=15)
    plt.scatter(outliers['x'],outliers['y'],edgecolor='red',s=15)
    plt.show()
    
    return df
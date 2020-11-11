import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.ensemble import IsolationForest


def isolation_forest(df, max_samples, random_state, contamination):
    
    # x ja y arvot talteen
    x_temp = df[['x','y']].values
    
    # Init minmaxscaler + fit+transform
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x_temp)
    
    # Normalisoidut arvot uuteen dataframeen
    xy_normalized = pd.DataFrame(x_scaled)
    xy_normalized = xy_normalized.rename(columns={0: 'x', 1: 'y'})
      
    # Isolationforest annetuin parametrein + fit
    clf = IsolationForest(max_samples=max_samples,random_state=random_state, contamination=contamination) 
    clf.fit(xy_normalized)
    
    # Outlier detect
    if_scores = clf.decision_function(xy_normalized)
    if_anomalies=clf.predict(xy_normalized)
    if_anomalies=pd.Series(if_anomalies).replace([-1,1],[1,0])
    if_anomalies=xy_normalized[if_anomalies==1]
    
    print('Dataframe lenght before:', len(df))
    
    # Drop outliers from df + reset index
    df = df.drop(df.index[if_anomalies.index.values])
    df = df.reset_index(drop=True)
    
    print('Dataframe lenght after:', len(df))
    print('Total outliers detected:', len(if_anomalies))
    
    # Plot results
    plt.gca().invert_yaxis()
    plt.scatter(df['x'],df['y'],edgecolor='black')
    plt.show()
    
    return df
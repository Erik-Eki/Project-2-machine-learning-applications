import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

def LOF(df, neighbours, leaf):
    
    df_original = df.copy()
    clean =[]
    outliers =[]
    x = 0
    # dividing data to chunks, to avoid loading all data into memory
    print("Starting...")
    print("Chunk size: ", len(df)/1000)
    # iterate through chunks
    for chunk in np.array_split(df, (len(df)/100)):
        
        # seperate the coordinates
        X = chunk[['x', 'y']].values

        # fit the model
        clf = LocalOutlierFactor(n_neighbors=neighbours, algorithm='auto', leaf_size=leaf)
        y_pred = clf.fit_predict(X)

        # map results
        X_normals = X[y_pred == 1]
        X_outliers = X[y_pred == -1]

        # Add good points to "clean" list
        clean.extend(X_normals.tolist())
        # Add outliers to "outliers" list
        outliers.extend(X_outliers.tolist())

        # Prints loading block to track progress per chunk
        b = "Loading... " + "#" * int(x / len(chunk))
        print (b, end="\r")
        x += 1
        
    df_clean = pd.DataFrame(clean, columns=['x','y'])
    df_outliers = pd.DataFrame(outliers, columns=['x','y'])
    
    print("Vanha taulu: ", len(df_original))
    print("Uusi taulu: ", len(df_clean['x'])) 
    print("Poistettuja pisteitä: ", len(df_original) - len(df_clean))
    total_data = len(df_original)
    total_missing = len(df_original) - len(df_clean)
    percentage = (total_missing/total_data) * 100
    percentage_remain = (1 - (total_missing/total_data)) * 100
    print("Percent removed:   ",round(percentage, 2),'%')
    print("Percent remaining: ",round(percentage_remain, 2),'%')
    print(f"{'-'*30}")

    return df_clean, df_outliers
    
# Draw the picture
def draw_LOF(df, outliers):
    plt.figure(figsize=(10,7))
    print("Printing the plot...")
    plt.title("Local Outlier Factor (LOF)")
    a = plt.scatter(df['x'], df['y'], c='white', edgecolor='k', s=15, alpha=0.5)
    b = plt.scatter(outliers['x'], outliers['y'], c='red', edgecolor='k', s=15, alpha=0.1)
    plt.axis('tight')
    plt.legend([a, b], ["Jääneet", "Poistetut"], loc="lower left")
    plt.show()

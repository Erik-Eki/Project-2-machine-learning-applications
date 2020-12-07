import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

def LOF(df, neighbours, leaf):
    df_temp = df.copy()
    clean =[]
    outliers =[]
    x = 0
    print("Starting...")
    print("Chunk size: ", len(df)/1000)
    for chunk in np.array_split(df, (len(df)/100)):
        
        X = chunk[['x', 'y']].values

        # fit the model
        clf = LocalOutlierFactor(n_neighbors=neighbours, algorithm='auto', leaf_size=leaf)
        y_pred = clf.fit_predict(X)

        # map results
        X_normals = X[y_pred == 1]
        X_outliers = X[y_pred == -1]
        #X_normals.uniques
        
        clean.extend(X_normals.tolist())
        #print(X_normals.tolist())
        outliers.extend(X_outliers.tolist())
        #np.concatenate([clean,X_normals])
        #np.concatenate([outliers,X_outliers])
        #np.append(clean, X_normals)
        #np.append(outliers, X_outliers)

        #print(f"Loading... {x}\r")
        b = "Loading... " + "#" * int(x / len(chunk))
        print (b, end="\r")
        x += 1
        
    df_clean = pd.DataFrame(clean, columns=['x','y'])
    df_outliers = pd.DataFrame(outliers, columns=['x','y'])

    return df_clean, df_outliers
    

def draw_LOF(df, outliers):
    print("Printing the plot...")
    plt.title("Local Outlier Factor (LOF)")
    #plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

    a = plt.scatter(df['x'], df['y'], c='white', edgecolor='k', s=20, alpha=0.5)
    b = plt.scatter(outliers['x'], outliers['y'], c='red', edgecolor='k', s=20, alpha=0.3)
    plt.axis('tight')
    plt.legend([a, b], ["Jääneet", "Poistetut"], loc="lower left")
    plt.show()

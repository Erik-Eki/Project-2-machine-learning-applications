LocalOutlierFactor
=

![](https://gitlab.dclabra.fi/wiki/uploads/upload_0c9849e37970df567c9deabb9c3effdb.png)

![](https://gitlab.dclabra.fi/wiki/uploads/upload_de7f3f3059bd23c6bfa024ba69f84f7b.png)


https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html

**LocalOutlierFactor**(*LOF*) on valvomaton outlierien tunnistus algorytmi.

Kunkin näytteen poikkeavuuspisteitä kutsutaan **Paikallisiksi Outlier-Tekijöiksi** (*Local Outlier Factor*). Se mittaa tietyn näytteen **tiheyden paikallista poikkeamaa naapureihinsa nähden**.

Se on *paikallinen*, koska poikkeavuuksien pisteet riippuvat kohteen eristämisestä ympäröivään naapurustoon nähden. Tarkemmin sanottuna: **k-nearest neighbourit antavat sijainnin, joiden etäisyyttä käytetään paikallisen tiheyden arvioimiseen.**

Vertaamalla näytteen paikallista tiheyttä naapureiden paikallisiin tiheyksiin voidaan tunnistaa näytteet, joilla on olennaisesti pienempi tiheys kuin naapureillaan. Näitä pidetään poikkeavina eli outliereina.

# LOF-funktio
```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

def LOF(df, neighbours, leaf):
    
    df_temp = df.copy()
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

    return df_clean, df_outliers
    
# Draw the picture
def draw_LOF(df, outliers):
    print("Printing the plot...")
    plt.title("Local Outlier Factor (LOF)")
    b = plt.scatter(outliers['x'], outliers['y'], c='red', edgecolor='k', s=20, alpha=0.3)
    a = plt.scatter(df['x'], df['y'], c='white', edgecolor='k', s=20, alpha=0.5)
    plt.axis('tight')
    plt.legend([a, b], ["Jääneet", "Poistetut"], loc="lower left")
    plt.show()
```

## Actual use
```python
# Returns the cleaned dataframe and outlier dataframe
# 
# Arguments: The dataframe to be cleaned, number of neightbours and the leaf size
df2, outlierit = LOF(df1, 10, 10)
# Draw the deleted and kept points
draw_LOF(df2, outlierit)

# Do some stuff to calculate the amount dropped.
df3 = df1[~df1.isin(df2)].dropna()
print("Alkuperäinen data:",len(df1))
print("Dataa jäljellä:",len(df3))
print("Poistetut outlierit: ",len(df1) - len(df3))
df1 = df3
```
```python
Starting...
Chunk size:  9711.058
Printing the plot...############################################################################################################################
```

![](https://gitlab.dclabra.fi/wiki/uploads/upload_e0321ac50220efd969734147fc8a79fc.png)

```
Alkuperäinen data: 9711058
Dataa jäljellä: 8624269
Poistetut outlierit:  1101034
Percent removed:    11.32 %
Percent remaining:  88.68 %

CPU times: user 3min 54s, sys: 10.1 s, total: 4min 4s
Wall time: 3min 53s
```

## Konkluusio

LocalOutlierFactor poistaa ihan hyvin outliereita myöskin kauppa-alueen sisältä. Tälläiset pisteet todennäköisesti ovat sellaisia, jotka eivät matchaa ympärillä olevien pisteiden tiheyden kanssa.

Poistettuja pisteitä oli 11.32% datasta eli 1/10 siivoutui pois.
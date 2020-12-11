# Regressiot


Haetaan DATAT taulusta reitti data Ipywidgetin avulla:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_0442e830d3497f36763d6aa2ea44d71e.PNG)


## LineaariRegressio

Otetaan kokonaismatka talteen:
```kokonaismatka = df.groupby(['ajokerta'])['distance'].sum().values```

Tehdään näistä featuret käyttäen df_to_features()-muuttujaa:

```python
features = df_to_features2(df)
features['distance'] = matka
```


![](https://gitlab.dclabra.fi/wiki/uploads/upload_f9fe9439fd497d134043934a19a18435.PNG)



### Outliers:
Otetaan outliereitä pois 'kesto' ja 'distance' sarakkeista käyttäen Z-scorea:

Lähtee hyvin parisensataa riviä.


### LineaariRegressioMalli



```python
import numpy as np
from sklearn.linear_model import LinearRegression

#fit model
model = LinearRegression()
model.fit(kesto, matka)

#squared score
r_sq = model.score(kesto,matka)
print('coefficient of determination:', r_sq)

# intercept ja slope
print('intercept:', model.intercept_)
intercept: 5.633333333333329
print('slope:', model.coef_)

```

#### Tulokset:

coefficient of determination: 0.02797703317771849
intercept: 205.39818661042213
slope: [0.01509046]

Näistä nähdään että lineaariregressio ei sovellu/ei ole tarpeeksi featureita ennustamaan kestoa matkasta.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_5cedfb24e8dba5c4c15c0308899f2181.PNG)

## Mikä on ennuste kauppareissun kestolle pe klo 16-17, kun kauppareissun pituus on keskipitkä?

Otetaan binseihin 'tosi lyhyt', 'lyhyt', 'normaali', 'pitkä', 'tosi pitkä'
```python
bins = [60,300, 900, 1500 , 3600, 7200]
#labels = ['lyhyt', 'normaali', 'pitkä', 'tosi pitkä']
labels = [1, 2, 3, 4, 5]
features['binned'] = pd.cut(features['kesto'], bins, labels=labels)
```

Fitataan tarvitavat featuret ja katsotaan ennustus ja tarkkuus
```python
model.fit(features[['dayofweek', 'current_hour', 'binned']].values, features.kesto)

y_pred = model.predict([[4,0,5]])

print(model.score(features[['dayofweek', 'current_hour', 'binned']].values, features.kesto))
print(y_pred)
```

Tarkkuudeksi saatiin: 0.827
Ja kauppareissun kestolle 3250s


## RandomForestRegressor

Laitetaan featuret X ja y muuttujiin:


```python
# X ja y featuret
X =  features.iloc[:, 3:5]
X['binned'] = features['binned']
y = features['kesto']
```


Jaetaan data train test:

```python
from sklearn.model_selection import train_test_split

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
```

Tehdään RandomForestRegressor-objekti ja fitataan se
```python
from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators=1, random_state=0)
regressor.fit(X_train, y_train)
```
 Otetaan tarkkuus testi datasta:
```p
regressor.score(X_test, y_test)
0.9034129073426067
```

R2 scoreksi saatiin 0.9 joka on kyl hyvä.

Testataan tätä koko datalle:
```r
regressor.score(X, y)
0.911004916671244
```
R2 scoreksi saatiin 0.91 joka on kyl hyvä.

Tästä vielä nähdään visuaalisesti ennustus vs todellinen data. Y-akselilla on binsit 1-5 jotka on labeloitu ylempänä. 4-binssissä eli 'pitkä' luokassa näyttää olevan eniten virhe ennustuksia.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_af71747f672b59ba195819895a306b5a.PNG)




# Isolation Forest TODO: node_id automatiosinti

Moduuli ottaa sisään (dataframen, random_staten, contamination, node_id)
- random_state = INT arvo
- contamination = tresholdi outlierien määritykseen

node_idt yksittäisinä koska järkevää jokaista nodea erikseen tarkastella

## 1. X ja Y arvot talteen, IsolationForest init ja fittaus

Max_samples annetaan kaikki data mitä tarjolla.
```python
# x ja y arvot talteen
x_temp = df.loc[df['node_id']==node][['x', 'y']]


# Isolationforest annetuin parametrein + fit
clf = IsolationForest(max_samples=len(x_temp),random_state=random_state, contamination=contamination) 
clf.fit(x_temp)
```


## 2. Outlierien määritys decision_funktiolla ja predictillä

Decision + predict funktioilla saadaan Isolation Forestista pisteet, jotka on luokiteltu outliereiksi. Haetaan kyseiset pisteet *x_temp* dataframesta ja tallennetaan ne *outliers* listaan

```python
# Decision funktio + predict
if_scores = clf.decision_function(x_temp)
if_anomalies=clf.predict(x_temp)

# Tallennetaan x_tempin arvot joissa if_anomalies on 1
if_anomalies=pd.Series(if_anomalies).replace([-1,1],[1,0])
if_anomalies=x_temp[if_anomalies==1]

# Tallenetaan outlierit omaan muuttujaan
outliers = x_temp.loc[if_anomalies.index.values]
```

## 3. Outlierien poisto *x_temp* dataframesta ja näiden arvojen merge alkuperäiseen *df* dataframeen

Lisätään muutama printtaus joissa näkyy alkuperäisen dataframen koko ennen ja jälkeen sekä outlierien tarkka määrä.

Poistetaan *x_temp*istä outlierit drop funktiolla käyttäen indeksejä.

Alkuperäisestä dataframesta haetaan kaikki *x_temp*issä olevat arvot, joista on siis poistettu outlierit

```python
print('Dataframe lenght before:', len(x_temp))

# Drop outliers from df + reset index
x_temp = x_temp.drop(x_temp.index[if_anomalies.index.values])

# Loc all values from original df that matcges x_temp values
df = df.loc[x_temp.index]
df = df.reset_index(drop=True)

print('Dataframe lenght after:', len(df))
print('Total outliers detected:', len(if_anomalies))

```


## 4. Scatterplotataan tulokset

Plotataan outlierit punaisella ja loput mustalla



```python
# Plot without outliers - black
plt.scatter(df['x'],df['y'],edgecolor='black',s=15)

#Plot outliers - red
plt.scatter(outliers['x'],outliers['y'],edgecolor='red',s=15)
plt.show()
```

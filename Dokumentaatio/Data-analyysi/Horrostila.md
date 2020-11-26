Horrostilat
=

Jossakin yhteiskatselmoinnista saatiin info, että nodet lähettävät dataa n. joka sekunti ja kun ne ovat olleet paikallaan 10 minuuttia, ne menevät horrostilaan eivätkä enää lähetä dataa.

Nämä paikoillaan olevat pisteet voisi etsiä ja poistaa

# Käyttö
```python
df1 = horrostila(df1)
df1
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_35984aa0e4a2dd433972ebab07136540.png)

# Etsitään nodet, jotka menevät horrostilaan
```python
import pandas as pd

def horrostila(df):
    # temp time_delta
    df['time_delta'] = df.timestamp.diff()
    
    # Boolean if timedelta >= 10
    df['Horrostila'] = df.time_delta.dt.seconds >= 10
    
    # drop temp time_delta
    df = df.drop(columns=['time_delta'])
    
    return df
```    

## Kuvaaja
```python
dftest = df1[df1['Horrostila'] == True]
print("Poistetut horrostilassa olevat nodet: ",len(dftest))
plt.scatter(df1['x'], df1['y'], c='coral', marker='s', s=10, alpha=0.3, label="Normaalit")
plt.scatter(dftest['x'], dftest['y'], c='cyan', marker='s', edgecolors="black",  s=10, alpha=0.3, label="Horrostilassa")
plt.title("Nodejen status")
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
```
```
Alkuperäiset nodet:  553983
Poistetut horrostilassa olevat nodet:  458319
Horrostilassa olevat nodet:  95664
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_44c6f8e88aaf092e2e6b4591f22fe4e9.png)


# Konkluusio

Kuvan perusteella voidaan päätellä, että kassoille jätetyt korit ja muut menevät horrostilaan, kuin myös kaupan sisäänkäynnillä odottavat. Mutta myös ilmeisesti kaupan sisällä on muutamia hylättyjä kärryjä/koreja.

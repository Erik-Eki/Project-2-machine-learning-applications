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
```Poistetut horrostilassa olevat nodet:  454```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_ff9d8c4c5dc6d6610ff570b135258847.png)

# Konkluusio

Kuvan perusteella voidaan päätellä, että kassoille jätetyt korit ja muut menevät horrostilaan, kuin myös muutamia hylättyjä kärrejä/koreja löytyy vähän ympäri kauppaa, muttei liian paljon.

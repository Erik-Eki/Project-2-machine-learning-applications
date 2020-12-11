Gridin karkeuden etsiminen
=

Optimaalisen gridin koon löytäminen onkin hyvin hankalaa: Niin ohjelmallisesti kuin myös visuaalisesti.

Ei voi olla oikein varma, että milloin gridi on tarpeeksi iso ettei yhtään dataan mene hukkaan tai milloin se on turhan iso.

Tässä kuitenkin vähän tajunnanvirtaa ja yritystä etsiä jonkin näköistä perustelua tulevaisuuden päätöksille.

# Datan jakaminen

Jaetaan taulu X:n ja Y:n, missä Y on piirre
```python
def table_to_XY(df):
    X = df.drop(['index', 'node_id', 'grid_id', 'timestamp', 'x_grid', 'y_grid'], axis=1)
    Y = df['grid_id']
    return X, Y
    
X, Y = table_to_XY(df1)
```
---

# K-means

Ideana oli siis käyttää K-mean:siä etsimään klusterien keskipisteet. Hypoteesi oli, että jos käytävä on klusteri ja otetaan sen keskipiste, saadaan tarkkaa piste käytävän keskipisteelle.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_b1d47f6de540a3552ced13e33130b2db.png)

Tämän takia, käytetään k-meansia hieman eri tarkoitukseen mitä yleensä:
Normaalisti etsittäisiin optimaalinen k:n arvo (joka oli 4 tälle datalle btw).

Mutta koska ei nyt ei kinosta klusterointi vaan ne keskipisteet, käytetään hyvin isoa k:n arvoa.

```python
from sklearn.cluster import KMeans


plt.set_cmap('winter')

# Opetetaan malli ja tehdään ennustus
est_kmeans = KMeans(n_clusters=200, init='k-means++')
est_kmeans.fit(X)
pred_kmeans = est_kmeans.predict(X)

# Clusterien keskipisteet
centers = est_kmeans.cluster_centers_

def draw_kmeans():
    plt.scatter(X['x'], X['y'], c=pred_kmeans)

    plt.scatter(centers[:, 0], centers[:, 1], c='deeppink', marker='*', s=50)
    plt.title("k-Means with 'k-means++'")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    
draw_kmeans()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_607a1e1e99202e7ea87d0d2dd218ed87.png)

Kuten kuvasta näkyy, klusterien keskipisteet näyttävät muodostavan suoria linjoja. Voidaan siis todeta että nuissa pinkeissä tähdissä seisotaan käytävän keskellä.

# Tehdään clusterien keskipisteistä gridi
```python
aisle = pd.DataFrame(centers, columns=['x', 'y'])
# Tehdään gridi
aisle = xy_to_grid(aisle, aisle.x, aisle.y, grid_size)
# Pudotetaan x ja y
aisle = aisle.drop(['x', 'y'], axis=1)
aisle.head()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_3c50e15d474832ab8b5198fb8299c0bb.png)

### Pyöritellään taulukoita oikeaan muotoon
```python
reitit_dropped = df_reitit.drop(['ajokerta', 'timestamp', 'node_id'], axis=1)
reitit_dropped.rename(columns = {'ID':'grid_id', 'x':'x_grid', 'y':'y_grid'}, inplace = True)
reitit_dropped
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_937743b844d35e446933a2cfb47b842a.png)


### Verrataan keskipisteitä reitteihin

Yhditetään keskipiste taulu reitti tauluun ja poistetaan dublikaatit. Näin löytyy reittien keskipisteet.
```python
df_yhdistetty = reitit_dropped.drop_duplicates().merge(aisle.drop_duplicates(), on=aisle.columns.to_list(), 
                                                  how='left', indicator=True)
print(df_yhdistetty['_merge'].unique())
#df2.loc[df2._merge=='left_only',df2.columns!='_merge']
df_yhdistetty = df_yhdistetty.loc[df_yhdistetty['_merge'] == 'both']
df2 = df_yhdistetty.drop(columns=['_merge'])

plt.scatter(reitit_dropped['x_grid'], reitit_dropped['y_grid'], c='black', marker='s', s=10, label="Reitit")
plt.scatter(df2['x_grid'], df2['y_grid'], c='deeppink', marker='o', s=50, label="Keskipisteet")
plt.title("Keskipisteet reiteillä")
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_3fa9c97dd621a91c34e1b0f4036e8db1.png)

Pisteet ovat siis reiteillä.

# Allstar labyrintti

Reiteissä on hypähdyksiä joissa ei ole dataa, mutta niitä pystyisi kyllä täydentämäänkin; Nimittäin Allstar-reitinhaulla.

- 1 on seinä/hylly/muu este
- 0 on käytävä tai alue, mistä voi kulkea
- 5 on startti
- 6 on maali

Sovitetaan nuo keskipisteet nyt matriisiin.

Luodaan ensin tyhjä matriisi jossa on vain 1:siä.

Sortataan myös keskipistetaulua, että se tulee oikein matriisiin. (Matriisin 0,0 kohta on vasemmassa yläreunassa, taulun 0,0 on vasemmassa alareunassa)
```python
table1 = np.ones((40,40), dtype=np.int16)

df2.sort_values(['x_grid', 'y_grid'], axis = 0, ascending = [True, True], inplace = True)
df2 = df2.drop(columns=['grid_id'])
df2
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_100d8cea04d0ceb95f474fe92caf9c51.png)


Ja tuon taulun perusteella, muutetaan esim. 0 rivillä 32 sarakkeesta ykkönen nollaksi edelle tehdyssä 40x40 1-matriisissa.
```python
for i, j in zip(aisle['x_grid'], aisle['y_grid']):
    table1[j][i] = 0

# Taulu printtautuu väärinpäin, joten flipataan se vain ympäri.
print('\n'.join(' '.join(str(cell) for cell in row) for row in np.flipud(table1)))
print(np.flipud(table1))
```

Lopputulos:
```python
1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 0 1 0 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1
1 1 1 0 1 1 1 0 1 1 0 1 1 1 1 1 0 1 1 1 1 1 0 1 1 0 1 1 1 0 1 1 1 0 1 1 1 1 1 1
1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 0 1 1 1
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1
1 1 0 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 1
0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 1 0 1 0 1 1
0 1 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 0 1 0 1 1 1 1
1 1 1 0 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 0 1 1
1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1 0 1 1 1
1 1 1 0 1 1 1 1 0 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 0 1 1 0 1 0 1
1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 0 1 0 1 1 1 1
1 1 1 0 1 1 1 0 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1
1 1 1 1 1 1 1 0 1 1 1 0 0 0 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 1 1 0 1 0 1
1 1 1 1 0 1 0 1 1 0 0 1 0 1 1 0 1 0 1 0 1 1 0 1 1 1 0 1 0 1 1 1 0 0 1 1 0 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 0 0 1 1 0
1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 0 1 1 1
1 1 1 1 0 1 1 1 1 1 1 0 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1 1 0 1 1 1
1 1 0 1 1 1 1 1 1 1 1 0 0 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 0 1 0 1 0 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 0 1 1 1
0 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 1 0 1 1 1 1 1 1 1 0 1 1 0 1 0 1 1 1 1 0 0 1 1
1 1 0 1 1 1 0 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 1 1
1 1 1 1 1 0 1 1 1 1 0 1 1 0 1 0 1 0 1 1 1 1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0 1 0 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1 1 1 0 0 1 1 0 0 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 0 1 1 0 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 0 1 0 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_410934ac0dc3bedbf710e66432f0a615.png)

Tässä vaiheessa pitää käyttää artistista vapautta ja katsoa missä suunnilleen voisi se käytävä olla. Joissakin kohtaa ilmiselvää, joissakin... Ei niinkään.

Manuaalisen editoinnin jälkeen:
![](https://gitlab.dclabra.fi/wiki/uploads/upload_cabc58838abeacf26167f12dbe87b149.png)

# Konkluusio

Idea oli ihan ok ja lopussa se auttoikin löytämään vähän tarkemmin missä käytävät oikein sijaitsevat.
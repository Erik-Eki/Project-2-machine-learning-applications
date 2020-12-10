Klusterointi
=

```python
df = database_query("SELECT * FROM DATA")
df
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_31662fb531076b2247c9d8ec8780af24.png)

Muutetaan "distance" niin, että jokaisen ajokerran pituudet on laskettu yhteen
```python
distances = df.groupby(['ajokerta'])['distance'].sum().to_dict()
df["distance"] = df['ajokerta'].map(distances()
```

Etsitään ideaali k:n arvo datasetille elbow-metodilla
```python
ideal_k(df)
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_417f02559699ce1e404c19dc65554142.png)

Create list, which lenght matches amount of grid_ids and check, which ids shopping trip does have in it.
```python
 In [4]:  %%time
grid = np.arange(0,1600,1)
kaikki = []
for ajo in df["ajokerta"].unique():

    kaynyt = []
    kerta = df[df["ajokerta"] == ajo]["grid_id"].unique() 
    [kaynyt.append(1) if x in kerta else kaynyt.append(0) for x in grid]
    kaikki.append(kaynyt)
```

Käytetään PCA:ta löytääksemme tunnukset, jotka selittävät yleisen varianssin kaikilla matkoilla.
```python
# https://etav.github.io/python/scikit_pca.html
import numpy as np
from sklearn.decomposition import PCA
pca = PCA(n_components=1600)
pca.fit(kaikki)

exp = pca.explained_variance_ratio_
var=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=3)*100)

plt.ylabel('% Variance Explained')
plt.xlabel('# of Features')
plt.title('PCA Analysis')
plt.ylim(30,100.5)
plt.style.context('seaborn-whitegrid')

plt.plot(var)
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_4063b8688d847854e2d5dd22484f679b.png)
```python
pca = PCA(0.9)
pca.fit(kaikki)

test  = pca.transform(kaikki)
print("original shape:   ", len(kaikki[0]))
print("transformed shape:", len(test[0]))
```
original shape:    1600
transformed shape: 363

Luo uusi datasetti PCA-komponenteista
```python
pca_features = pd.DataFrame(data = test, columns = [f"{x}" for x in np.arange(0,len(test[1]),1)])
pca_features
```

Luodaan waypointit piirrematriisiin
```python
def df_to_features(df):
    df["check"] = df["ajokerta"].shift(1)
    uniques = df["ajokerta"].unique()
    rivit = []
    asd = pd.DataFrame()
    for row in df.itertuples():
        if row.ajokerta != row.check:
            rivit.append({"ajokerta":row.ajokerta, 
                          "node_id":row.node_id, 
                          "kesto":row.kesto, 
                          "dayofweek":row.dayofweek,
                          "current_hour":row.current_hour, 
                          "distance":row.distance})
            
    return pd.DataFrame(rivit)
features = df_to_features(df)

print(len(features))
print(len(pca_features))
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_010d9f5383c2b64ed9bec9b40a997378.png)

Tästä on sitten tehty moduuli **df_to_features()**, joka lisää waypointit piirrematriisiin
```python
df = df_to_features(df)
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_7ffc8e44a57a9c56a96d8064c1dbb486.png)


## K-Means Clustering
[Number of clusters](https://towardsdatascience.com/cheat-sheet-to-implementing-7-methods-for-selecting-optimal-number-of-clusters-in-python-898241e1d6ad)
### Elbow Method
```python
kmeans = KMeans()
# k is range of number of clusters.
visualizer = KElbowVisualizer(kmeans, k=(2,30), timings= True)
visualizer.fit(std_df)        # Fit data to visualizer
visualizer.show()       # Finalize and render figure
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_c30bdd8a6ae841c041128920412651fe.png)

Kuten näkyy, optimaalisin k:n arvo on 9

Silhouette Score
```python
# k is range of number of clusters.
visualizer = KElbowVisualizer(kmeans, k=(2,30),metric='silhouette', timings= True)
visualizer.fit(std_df)        # Fit the data to the visualizer
visualizer.show()      # Finalize and render the figure
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_068bc45f39b7144e0807f084fd0d5990.png)

Siluetilla k:n arvoksi saatiin 8

## K-Medoids
Tähän tarvitsee asentaa: ```pip install scikit-learn-extra```

Klustereiden määrä
### Elbow Method
```python
from sklearn_extra.cluster import KMedoids
kmetoids = KMedoids()
# k is range of number of clusters.
visualizer = KElbowVisualizer(kmetoids, k=(2,15), timings= True)
visualizer.fit(std_df)        # Fit data to visualizer
visualizer.show()        # Finalize and render figure
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_71142864383be1450c10760beaa9965a.png)

### Silhouette Score
```python
# k is range of number of clusters.
visualizer = KElbowVisualizer(kmetoids, k=(2,15),metric='silhouette', timings= True)
visualizer.fit(std_df)        # Fit the data to the visualizer
visualizer.show()       # Finalize and render the figure
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_0bfe6de2dd2acf57a773cf71356f889e.png)

### Calinski Harabasz Score
```
visualizer = KElbowVisualizer(kmetoids, k=(2,15),metric='calinski_harabasz', timings= True)
visualizer.fit(std_df)        # Fit the data to the visualizer
visualizer.show()    # Finalize and render the figure
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_60bcef82c127f7e48fd41d2dad7cbd20.png)

---


## Reittien klusterointi

Ideanahan tässä on siis **erotella reittejä eri piirteiden mukaan**. Lopputuloksena pitäisi olla kuvaaja, jossa samankaltaiset reitit on eroteltu omiin klustereihin.

Klusteroidaan reitit, niin että **päivä korreloisi reitin keston kanssa**
```python
from sklearn.cluster import AgglomerativeClustering

potato = df2[['ajokerta','dayofweek','kesto']]

# Käytetään Agglomeratiivista klusterointia
cluster = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
y_kmeans = cluster.fit_predict(potato)

potato["predicted"] = y_kmeans

ajot = df2["ajokerta"].unique()
oltava =  potato.index.unique()

poistettavat = set(ajot)-set(oltava)

data = potato[~potato['ajokerta'].isin(poistettavat)]
data["pred"] = None

zip_iterator = zip(oltava, y_kmeans)
parit = dict(zip_iterator)

df_pred = df.copy()
df_pred['pred'] = df_pred["ajokerta"].map(parit).fillna(data["pred"])
df_pred['predicted'] = df_pred["ajokerta"].map(parit).fillna(data["predicted"])
data['pred'] = data["ajokerta"].map(parit).fillna(data["pred"])
data
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_33af40a272a5a59f6906aab602467b7a.png)

Tiputetaan ajokerrat, jotka ei klusteroituneet
```python
df_pred = df_pred.dropna()
df_pred
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_fb66b7c342da800c54c939d450069ef9.png)
- **8335 rows × 12 columns vs. 6420 rows × 15 columns**

Piirretään klusteroidut ajokerrat:
```python
def draw_cluster_route(df, column, huem amount_colum):
    ajot = df[column].unique()
    print(ajot)
    ajot_len = len(df[column].unique())

    print("Ajokerrat: ",ajot_len)
    
    Cols = amount_colum

    Rows = ajot_len // Cols 
    Rows += ajot_len % Cols
    
    Position = range(1,ajot_len + 1)
    
    fig = plt.figure(1,figsize=(30,15))
    
    plt.rcParams['figure.facecolor'] = 'black'
    for i, k in zip(ajot, range(ajot_len)):
        ax = fig.add_subplot(Rows,Cols,Position[k])
        # Käytetään tätä jos halutaan piirtää ajokerrot eroteltuina
        sns.scatterplot(x="x", y="y", data=df[df[column] == i],  hue=hue, markers=False, size=30, legend='full', palette="rainbow", ax=ax)
        
        # Käytetään tätä jos halutaan piirtää ilman eroteltuja ajokertoja
        '''ax.plot(df[df[column] == i]['x'], df[df[column] == i]['y'], c=df['ajokerta'])#np.random.random(3)'''
        
        ax.set_title(f"Klusteri: {i}",color="white")
        ax.grid(color='white', linestyle='--', linewidth=1, alpha=0.5)
        ax.set_facecolor('xkcd:black')
        #ax.autoscale(enable=True)
        ax.legend(loc='lower left',fontsize=8)
        
    plt.suptitle("Kesto & viikonpäivä klusterointi",color="white")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
```
```python
draw_cluster_route(df_pred, 'predicted', 'ajokerta')
```
Piirrematriisi (Ajoreitit eri väreillä:
![](https://gitlab.dclabra.fi/wiki/uploads/upload_29c6c3f56766f08bcbe12b964cef8c15.png)

Piirrematriisi (Vain samankaltaiset reitit)
![](https://gitlab.dclabra.fi/wiki/uploads/upload_318f612cfd2004acadb0c38cf213b1e4.png)


### Konkluusio
Klusterointi toimii ja on selvästi erotellut samankaltaiset reitit toisistaan viikonpäivän ja reitin keston perusteella. Mutta kuten näkyy, yhdelle klusterille ei löydy mitään.

Jos katsoo ```df_pred['predicted'].unique()```,
saadaan ```[ 5.  2.  6.  0.  1.  4. nan]```, Eli 3 ei klusteroidu

Esim. taulu, jossa vain "x", "y" ja "predicted"
![](https://gitlab.dclabra.fi/wiki/uploads/upload_8e48af1245db9543a032b8b1b38754dd.png)

### Kehitettävää
Ei ehditty tänne asti, mutta:

Ei nyt oikein tiedetä, että MIHIN reitit on klusteroitu. "Viikonpäivän ja keston mukaan", mutta missä klusterissa on mikä viikonpäivä? Entäs kesto? Onko kesto siis pitkä vai lyhyt?

## Reittien osien klusterointia

Tässä ideana oli klusteroida itse reittejä, jos niistä löytyisi jotkin alueet jotka korreloisivat (esim. vasen yläkulma olisi reiteissä suht saman kokoinen)

```python
import matplotlib.colors as pltc

def draw_cluster(df, column):
    ajot = df[column].unique()
    ajot_len = max(df[column].unique())

    print("Ajokerrat: ",ajot_len)
    
    Cols = 6

    Rows = ajot_len // Cols 
    Rows += ajot_len % Cols
    
    Position = range(1,ajot_len + 1)
    
    plt.figure(figsize=(20,10),facecolor=(1, 1, 1))

    for i,k in zip(ajot,range(ajot_len)):
        df_temp = df[df[column] == i][['x', 'y']]
        cluster.fit_predict(df_temp)
        plt.subplot(Rows,Cols,Position[k])
        plt.scatter(df_temp.iloc[:,0], df_temp.iloc[:,1], c=cluster.labels_, cmap='rainbow')
        plt.title(f"Reitti {i+1}")
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    
draw_cluster(df_pred,'ajokerta')
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_3c1fb8aa278c2d64a773c535d2831fd7.png)

### Konkluusio

Jotkin alueet reiteissä näyttäisivät klusteroituvan suurinpiirtein samoihin kohtiin (HUOM. värit muuttuu eikä ne ilmoita kolleroinnista), mutta ne ovat silti vähän liian hajanaisia ja muuttuvat liikaa.

### DBSCAN

PCA jakaa datapisteet useisiin tiettyihin eriin tai ryhmiin siten, että samojen ryhmien datapisteillä on samanlaiset ominaisuudet ja datapisteet eri ryhmissä niillä on jossain mielessä erilaisia ominaisuuksia.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

X= df_ajokerta[['x', 'y']]

def dbscan(X, eps, min_samples):
    ss = StandardScaler()
    X = ss.fit_transform(X)
    db = DBSCAN(eps=eps, min_samples=min_samples)
    db.fit(X)
    y_pred = db.fit_predict(X)
    plt.figure(figsize=(20,10))
    plt.scatter(X[:,0], X[:,1],c=y_pred, cmap='Dark2', s = 50)
    plt.title("DBSCAN")
    
dbscan(X, 0.10, 20)
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_272a50620ef06ffdaf985fdf120a9a50.png)

Aika epäselvää tulee. Kokeillaan eri tavalla:

```python
from sklearn import metrics
from sklearn.datasets import make_blobs


X = StandardScaler().fit_transform(X)

# Compute DBSCAN
db = DBSCAN(eps=0.15, min_samples=100).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))


# Plot result
import matplotlib.pyplot as plt
plt.figure(figsize=(20,10))
# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
```
```
Estimated number of clusters: 8
Estimated number of noise points: 3647
Silhouette Coefficient: -0.264
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_fed76f229298dfec383b007b99b0ac73.png)

#### Konkluusio
DBSCAN löysi pari kohtaa, missä pisteet ovat smankaltaiset. Ilmesesti ei sisäänkäynnillä eikä kassoilla ole samankaltaisia pisteitä vaikka luulisi, mutta alussa muuten näyttäisi olevan jotain samankaltaisuuksia.

### Dendogrammi

[Pöllitty sciPy sivuilta](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html)

- Dendrogrammi havainnollistaa, kuinka kukin klusteri koostuu piirtämällä U-muotoinen linkki ei-yksittäisen klusterin ja sen lasten välille. 
- U-lenkin yläosa osoittaa klusterin sulautumisen.U-lenkin kaksi osaa osoittavat, mitkä klusterit yhdistettiin. U-lenkin kahden haaran pituus edustaa lapsiklustereiden välistä etäisyyttä. 
    - Se on myös kofeneettinen etäisyys kahden lapsiryhmän alkuperäisten havaintojen välillä.

Katsotaan miten reitin matka ja tunti klusteroituvat:
```python
from scipy.cluster import hierarchy

# generate the linkage matrix
X = df2[['distance', 'current_hour']]
#X = df2
Z = linkage(X,
            method='complete',  # dissimilarity metric: max distance across all pairs of 
                                # records between two clusters
            metric='euclidean'
    )                           # you can peek into the Z matrix to see how clusters are 
                                # merged at each iteration of the algorithm

# calculate full dendrogram and visualize it
plt.figure(figsize=(30, 10))
dn = hierarchy.dendrogram(Z)

hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
dn1 = hierarchy.dendrogram(Z, ax=axes[0], above_threshold_color='y',
                           orientation='top')
dn2 = hierarchy.dendrogram(Z, ax=axes[1],
                           above_threshold_color='#bcbddc',
                           orientation='right')
hierarchy.set_link_color_palette(None)  # reset to default after use
plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_b138df7a7241f8376ac0fbcb55625b99.png)

Reitin matka ja tunti erottui 3 klusteriin, joissa yhteensä 25 osaa.
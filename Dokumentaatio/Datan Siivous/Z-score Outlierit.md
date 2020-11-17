Datan Siivous - Z-score Outlierit
=

**(Huom. Esimerkeissä testaus tehty 1 000 000 datapisteellä.**)


Meillä on monta eri tapaa mietitty, että miten poistaa outliereita.

Tämä oli yksi ensimmäisistä ja se on suhtkoht yksinkertainen:

Se etsii outliereita laskemalla z-scoren katsomalla x ja y kolumneja.

Tässä sitten se tosin, ettei se etsi outliereita ollenkaan esim. timestampin perusteella, mutta näin se vaikuttaisi järkevimmältä tässä vaiheesssa.

# Alkuvalmistelut
Importtaus:
```python=
from outliers import find_outliers, draw_histogram
```

Eli importataan paketti "outliers" ja sieltä kutsutaan kaksi funktiota: find_outliers ja draw_histogram

# Outliers.py
Käydäänpäs nopiaa läpi mitä outliers.py:ssä oikein tapahtuu:

## Importoinnit
```python=
# Imports
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from scipy.stats import zscore
import numpy as np
import pandas as pd
```

## Histogrammi outliereista

![](https://gitlab.dclabra.fi/wiki/uploads/upload_d481b4c4002862e73fffcea2065a20a3.png)

Histogrammi outliereista auttaa siinä mielessä, että sen *hännissä* yleensä näkee outlierit.

**Häntä** on siis keskittymän reunoilla tai ulkopuolella esiintyviä pisteitä.

Histogrammin piirtämiseen tarvitaan pari muuttujaa:
- Keskiarvo
- Normaalijakauma
- Bins
    - Kuinka monta "palkkia" histogramissa on (ns. karkeus)

Näitä tarvitaan myös normin todennäköisyystiheys-viivan laskemiseen
```python=
# Esim: draw_histogram(df2['x'], df2['y'], 20)
def draw_histogram(x, y, bin_num):
    plt.figure(figsize=(15,10))
    # mean of distribution
    mu = np.mean(x)
    mu2 = np.mean(y)
    print("x mean: ", mu)
    print("y mean: ", mu2)

    # standard deviation of distribution
    sigma = np.std(x)
    sigma2 = np.std(y)
    print("x std: ", sigma)
    print("y std: ", sigma2)

    # bins
    num_bins = bin_num

    # the histogram of the data
    n, bins, patches = plt.hist(x, num_bins, density=1, facecolor='orange', alpha=0.5, label='x')
    n2, bins2, patches2 = plt.hist(y, num_bins, density=1, facecolor='blue', alpha=0.5, label='y')

    # add a 'best fit' line
    y = norm.pdf(bins, mu, sigma)
    y2 = norm.pdf(bins2, mu2, sigma2)

    # This is what it norm.pdf does
    #y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    #y2 = ((1 / (np.sqrt(2 * np.pi) * sigma2)) * np.exp(-0.5 * (1 / sigma2 * (bins2 - mu2))**2))

    plt.plot(bins, y, 'r', alpha=0.8, label='x')
    plt.plot(bins2, y2, 'b', alpha=0.8, label='y')

    plt.title("Histogrammi lmao (bins %s)" % num_bins)
    plt.xlabel("Arvo")
    plt.ylabel("Tiheys")
    plt.legend()
    # Tweak spacing to prevent clipping of ylabel
    plt.tight_layout()
    plt.savefig('outliers-histogram.jpg')
    plt.show()
```

### Kuvaaja
- x arvot ovat oranssilla
    - x:n tiheyskäyrä on punaisella
- y arvot ovat sinisellä
    - y:n tiheyskäyrä on tummansinisellä

```
x mean:  2007.42516
y mean:  524.458634
x std:  880.5673627763946
y std:  1056.1131432857248
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_d09f76e2cef8261de56edb39a91e3463.png)


**Kuvasta voidaan päätellä, että:**
- X:llä **eniten arvoja** löytyy 1000-2000 ja juuri alle 3000 kohdilta
    - Käyrän hännässä on muutamia pisteitä **vasemmalla**
    - Käyrän huippu on **2000** kohdalla
- Y:llä **eniten arvoja** löytyy n. 0 ja -400 väliltä kohdilta
    - Käyrän hännässä on muutamia pisteitä **oikealla**
    - Käyrän huippu on **n. 700** kohdalla

Eli outliereita ei pitäisi olla kovinkaan paljon, olisiko parisataa.
Katsotaanpas seuraavassa osiossa tämä numeerisesti.

---

## Outliereiden etsiminen & poistaminen

Aluksi printtaillaan vähän, että mitä datassa nyt on:
```python=
def find_outliers(df):
    # Check for missing values
    missing_count = df.isnull().sum()
    print("Number of missing variables in table\n", missing_count)

    # Check for unique values in columns
    print(f"{'-'*30}\nUnique values in columns\n")
    print("uniques in x",len(df['x'].unique()))
    print("uniques in y",len(df['y'].unique()))
    print("uniques in z",len(df['z'].unique()))
    print("uniques in q",len(df['q'].unique()))


    print(f"{'-'*30}\nChecking z and q columns\n")
    print("uniques in z",df['z'].unique())
    print("uniques in q",df['q'].unique())


    # Checking how many different nodes
    amount_nodes = len(df["node_id"].unique())
    print(f"{'-'*30}\nNumber of nodes: {amount_nodes}")
```
Ulostulo näyttää tältä:
```
Number of missing variables in table
 node_id      0
timestamp    0
x            0
y            0
z            0
q            0
dtype: int64
------------------------------
Unique values in columns

uniques in x 5161
uniques in y 5033
uniques in z 1
uniques in q 1
------------------------------
Checking z and q columns

uniques in z [100]
uniques in q [0]
------------------------------
Number of nodes: 3
```

### Z-score

Z-score on numeerinen mittaus, joka kuvaa **arvon suhdetta arvoryhmän keskiarvoon**.
Z-score mitataan **keskihajannoilla** keskiarvosta.

- Jos Z-score on **0**, se osoittaa, että datapisteen pisteet ovat **identtiset** keskimääräisten pisteiden kanssa. 
- Jos Z-score on **1**, se merkitsee arvoa joka on **yhden keskihajonnan päässä** keskiarvosta. 

Z-score voivat olla positiivisia tai negatiivisia, ja positiivinen arvo osoittaa, että pisteet ovat keskiarvon yläpuolella, ja negatiiviset pisteet osoittavat, että ne ovat keskiarvon alapuolella.

Joten: Nyt lasketaan itse se z-score datalle:
```python=
    # Only use the x and y columns
    df1 = df[["x","y"]]

    z_scores = zscore(df1)
    abs_z_scores = np.abs(z_scores)
    
    # Remove rows that have outliers in at least one column
    outliers = df1[(abs_z_scores <= 2.5).all(axis=1)]
    
    # Pidä vain ne rivit, jotka ovat +3 - -3 keskihajonnan sisällä.
    filtered_entries = (abs_z_scores <= 2.5).all(axis=1)
    df_clean = df[filtered_entries]
    

    # pd.concat lisää kaksi DataFrame-kehystä yhteen liittämällä ne peräkkäin.
    # jos on päällekkäisyyksiä, se kaapataan drop_duplicates:illa
    # drop_duplicates oletusarvoisesti jättää ensimmäisen havainnon ja poistaa kaikki muut havainnot.
    # Tässä tapauksessa haluamme, että jokainen kaksoiskappale poistetaan. Siksi keep = False parametri
    potato = pd.concat([df1, outliers]).drop_duplicates(keep=False)

    print(f"{'-'*30}\nOutliers\n")
    print("Data with outliers: ", len(df))
    print("Ouliers removed:    ", len(df) - len(df_clean))
    print("Data after: ", len(df_clean))
```
Ulostulo:
```
------------------------------
Outliers

Data with outliers:  1000000
Ouliers removed:     6483
Data after:  993517
```
Kuten aavistelin viime histogrammin kohdalla, outliereita ei pitäisi olla kuin parisataa ja kuten näkyy: 173 outliereita löydetty.

Piirretään kuva poistetuista pisteistä:
```python=

    import matplotlib.pyplot as plt
    plt.gca().invert_yaxis()
    plt.plot(df_clean["x"], df_clean["y"], color="red", marker='o', linestyle='dashed', linewidth=0.2, markersize=3)
    plt.plot(potato["x"], potato["y"], color="blue", marker='x', linestyle='dashed', linewidth=0.2, markersize=3)
    plt.savefig("outliers-in-data.png")
    plt.show

    return df_clean
```
### Kuvaaja
Punaisella jääneet pisteet, sinisellä poistetut
![](https://gitlab.dclabra.fi/wiki/uploads/upload_a695065de04724b4dd2498967c8e0a76.png)


***(Huom. kuvaaja on todennäköisesti väärinpäin, mutta ilman pohjapiirustusta ei voi olla täysin varma)***

Kuvaajasta voidaan päätellä, että selvästi keskittymän ulkopuolella olevat pisteet on poistettu, kuten myös aika suoralta reunalta.

Tästä voidaan päätellä tuossa suoralla kohdalla olevan seinä.

# Konluusio

'z' ja 'q' kolumnit ovat siis aika turhia datassa, "korkeus" ei muutu kuin suurilla hypyillä ja "signaalin laatu" ei vaihdu ollenkaan.

Myöskään outliereita ei löydy z-score tekniikalla paljoa, eli tämä voisi olla vaikka se ***ensimmäinen läpikäynti datalle***, jossa poistetaan kaikkein röyhkeimmät outlierit.

Kuvaajasta voidaan päätellä jo kaupan suhteellinen muoto. Siitä myös näkee, missä eniten vääränlaisia tietoja syntyy.
Tuo "uloke" vasemmalla saattaisikin olla kaupan ulkopuolella oleva kärriparkki.
Mutta mitään ei voi olettaa ennenkuin saadaan käsiin pohjapiirrustus.
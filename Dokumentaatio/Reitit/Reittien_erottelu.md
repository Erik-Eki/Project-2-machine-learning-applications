Kauppareittien erottelu
====
## Moduulin kuvaus

Moduulissa olevalla luokalla ja funktioilla saadaan erotettua yksittäiset kauppareissut diskretioidusta Pandas DataFramesta. Lopputuloksena saadaan uusi Pandas Dataframe, johon on yhdistetty kaikki yksittäiset kauppareissut.



## Edellytykset 
- Dataframen täytyy olla diskretioisu [xy_diskretiointi](https://gitlab.dclabra.fi/ryhm-fox/projekti-2-team-fox/-/blob/master/Dokumentaatio/Gridin%20karkeuden%20etsiminen/XY_Diskretisointi.md)-moduulilla, jotta se sisältää grid_id-sarakkeen.
- Diskretioidusta datasta täytyy olla etsittynä kaupan [sisäänkäynnin sekä kassojen](https://gitlab.dclabra.fi/ryhm-fox/projekti-2-team-fox/-/blob/master/Dokumentaatio/Data-analyysi/Sis%C3%A4%C3%A4n_ja_ulosk%C3%A4ynnit.md) koordinaatit. Näiden koordinaattien pohjalta luodaan kummallekkin alueelle omat listat, joihin lisätään [ID-arvoiksi]() muutetut sijainnit.

Käytettävä dataframe näyttää aluksi tältä:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_634b03edd9adf02072eabf1b7f1fab75.png)


## Tarvittavat kirjastot

```
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set();
```

## Reitti -luokka

Tällä luokalla luodaan jokaiselle kauppareissulle oma objekti, johon tallennetaan reitin yksilöivä ID, korin node_id, reitin aikana kerätyt timestampit, ja datapisteiden sijainnit sekä x- ja y-koordinaatteina, että gridin ID-muodossa.


```
class Reitti:
    """[Objektiin tallennetaan yksittäisen reitin tiedot]
    """
    def __init__(self):
        """[Jokaiselle tallennettavalle tiedolle luodaan oma lista, kun objekti luodaan]
        """
        # ajokerta on reitin yksilöivä ID
        self.ajokerta = []
        self.node_id = []
        self.timestamp = []
        self.x = []
        self.y = []
        # Sijainti Grid ID
        self.ID = []
      
        
    def lisaa(self,ajokerta, node_id, timestamp, ID, x, y):
        """[Lisätään kerättävät tiedot yksitellen kauppareissu-objektin tietoihin.]

        Args:
            ajokerta ([list]): [yksittäisen reitin id]
            node_id ([list]): [yksittäisen reitin node_id]
            timestamp ([list]): [yksittäisen reitin timestampit]
            ID ([list]): [yksittäisen reitin kulkemat ID:t]
            x ([list]): [yksittäisen reitin x-koordinaatit]
            y ([list]): [yksittäisen reitin y-koordinaatit]
        """
        self.ajokerta.append(ajokerta)
        self.node_id.append(node_id)
        self.timestamp.append(timestamp)
        self.ID.append(ID)
        self.x.append(x)
        self.y.append(y)

```

## Datan lisääminen Reitti-objektiin.
- Diskretisoitu DataFrame käydään rivi-riviltä läpi.
- Boolean-muuttuja "matkalla" muutetaan arvoon True, kun iteroitavan rivin grid_id vastaa sisäänkäyntiä vastaavaa grid_id:tä 
  - (varmistetaan myös. että näitä rivejä on useampi peräkkäin, jotta yksittäiset alueelle tulevat signaalivirheet eivät vaikuta). 
   - Matkalla muuttujan täytyy olla False, jotta se voidaan muuttaa True:ksi. (Näin varmistetaan, että kauppareissu on päättynyt kassoille, ennen kuin uuden reissun tietoja aletaan tallentamaan)
- Jos iteroitavan rivin grid_id vastaa kassa-alueen grid_id:tä, asetetaan matkalla-muuttuja arvoon False. 
    - (Taas tarkistetaan, että useampi rivi peräkkäin on tällä alueella.)
- Reitti objektiin tallennetaan riviltä löytyvät tiedot, kun iteroitavan rivin grid_id ei vastaa kassa-aluetta tai sisäänkäyntialuetta, sekä matkalla muuttuja on tosi.
- Uusi Reitti-objekti luodaan, kun matkalla-muuttuja on False, ja saavutaan sisäänkäyntialueelle. Reitin yksilöivää ajokerta-muuttujaan muutetaan myös.
- Jokainen Reitti-objekti tallennetaan listaan, josta ne saadaan jatkokäsiteltäväksi.
  

Tällä tavalla saadaan tarkasti erotettua kauppareissut toisistaan, mutta menetelmä on verrattain hidas.

```
def erottele_reitit(df, in_ID, out_ID):
    """[Iteroi jokaisen dataframen rivin, tutkii milloin uusi kauppareissu alkaa ja lisää reissun tiedot sille luotuun objektiin.]

    Args:
        df ([DataFrame]): [Diskretisoitu dataframe]
        in_ID ([list]): [Sisäänkäyntialueen diskretisoidut koordinaatit ID-muodossa.]
        out_ID ([list]): [Kassa-alueen diskretisoidut koordinaatit ID-muodossa.]

    Returns:
        [list]: [Sisältää yksittäisten reittien objektit.]
    """
    
    # Luodaan dataframeen sarakkeet, joilla seurataan onko rivin paikkakoordinaatit kassa- tai sisäänkäyntialueilla.
    df["IN"] = df["grid_id"].isin(in_ID)
    df["OUT"] = df["grid_id"].isin(out_ID)

    # Näiden avulla seurataan, että useampi peräkkäinen rivi on kassa- tai sisäänkäyntialueilla.
    df['fo_IN'] = df['IN'].shift(5)
    df['fo_OUT'] = df['OUT'].shift(10)

    cleaned_xy = df.copy()
    erotellut_reitit = []      #tähän tallennetaan erotellut kauppareissut
    ajokerta = 0   # pidetään kirjaa kuinka monta kertaa kärry on ajanut kaupan läpi. Käytetään Kärryjen etsimiseen ja erotteluun
    reitti = Reitti()      #luodaan karry
    erotellut_reitit.append(reitti)     #lisätään ensimmäinen karry listaan, koska data alkaa yleensä kesken ajokerran 
    matkalla = False    

    
    for row in df.itertuples():
        
        if matkalla == False and row.IN  == True and row.IN == row.fo_IN:
            # Aloitetaan matka ja luodaan uusi olio kaupparaissulle.
            matkalla = True
            ajokerta += 1
            reitti = Reitti()      
            erotellut_reitit.append(reitti)

        elif row.OUT == True and row.OUT == row.fo_OUT:
            matkalla = False
        
        elif matkalla == True:
            erotellut_reitit[ajokerta].lisaa(ajokerta, row.timestamp,row.node_id,row.grid_id, row.x_grid, row.y_grid)
    
    return erotellut_reitit
```


## Reittien poistaminen

Reitti-objekteja voidaan poistaa listasta, jos se nähdään tarpeelliseksi.
Parametrina annetaan, kuinka monta datapistettä reitillä täytyy vähintään olla, jotta se pysyy listalla.

```
def poista_lyhyet_reitit(reitit, minimi_määrä_dataa):
    """[Poistaa kauppareissut, joissa annettua arvoa pienempi määrä dataa.]

    Args:
        reitit ([list]): [Sisältää kauppareissu-objektit]
        minimi_m ([int]): [Vähittäismäärä datapisteita objektissa.]

    Returns:
        [list]: [Palauttaa listan, jossa tarpeeksi datapisteitä sisältävät kauppareissut.]
    """
    clean_list = []
    for i in range(len(reitit)):
        if len(reitit[i].node_id) > minimi_määrä_dataa:
            clean_list.append(reitit[i])
    return clean_list
```

## DataFrame Reitti-objekteista

Kun kaikki data on saatu eristettyä omiksi reiteiksi, voidaan jokainen reitti-objekti käydä yksitellen läpi, ja yhdistää sen sisältämät tiedot omaksi dictionaryksi. Jokaisen objektin dictionarystä muodostetaan vuorollaan DataFrame, joka lisätään yhteen isoon DataFrameen, joka lopulta sisältää kaikkien reitti-objektien datat.

```
def reitit_dataframeksi(reitit):
    """[Luo dataframen, joka sisältää kaikkien kauppareissujen tiedot.]

    Args:
        reitit ([List]): [Sisältää kauppareissu-oliot]

    Returns:
        [DataFrame]: [Palauttaa Dataframen, joka sisältää jokaisen datasta erotellun kauppareissun.]
    """


    kauppareissut = pd.DataFrame(None,None,None,None,None)
    # käysään kaikki reittiobjektit läpi ja muodostetaan lisätään ne vuorollaan dataframeen.
    for kauppareissu in reitit:
        kauppareissu.yhdista_tiedot()
        reitti = pd.DataFrame(kauppareissu.tiedot)
        # Lisätään kaikki ajokerrat vuorollaan dataframeen.
        kauppareissut = kauppareissut.append(reitti,  ignore_index=True)
    return kauppareissut
```

Yksittäisistä kauppareiteista muodostettu dataframe näyttää tältä:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_4b9d2fd5db22b116b92ada65d6bd8587.png)

### Reittien visualisoiminen

Kaikki reitit saadaan visualisoitua yhdessä kuvaajassa
```

def plot_all_routes(df_reitit, grid_size):
    """Plottaa kaikki erotellut reitit samaan kuvaajaan]

    Args:
        df_reitit ([DataFrane]): [Sisältää erotellut reitit]
        grid_size ([int]): [Gridin koko on määritelty arvon mukaan.]
    """
    facet = sns.scatterplot(x="x", y="y", data=df_reitit, hue="ajokerta")
    facet.set_xticks(np.arange(0, grid_size+1,10))
    facet.set_yticks(np.arange(0, grid_size+1,10))
    plt.show()
```

![](https://gitlab.dclabra.fi/wiki/uploads/upload_06be2ff0795b3b9a3356af64a197bd99.png)

Kaikki reitit saadaan myös visualisoitua yksitellen. Kuvaajassa näkyy myös sisäänkäynti- ja kassa-alueet.
```
def plot_unique_routes(df_reitit, grid_size, in_x, in_y, out_x, out_y):
    """[Plottaa jokaisen kauppareissun peräkkäin.]

     Args:
         df_reitit ([DataFrame]): [Sisältää erotellut kauppareitit]
         grid_size ([int]): [Asettaa kuvaajan koon gridin koon mukaan..]
     """
    ajot = df_reitit["ajokerta"].unique()
    df_reitit["color"] = np.arange(0,len(df_reitit),1)
    for ajo in ajot:
        print(len(df_reitit[df_reitit["ajokerta"] == ajo]))

        facet = sns.scatterplot(x="x", y="y", data=df_reitit[df_reitit["ajokerta"] == ajo],  hue="color")
        sns.scatterplot(x=in_x, y=in_y)
        sns.scatterplot(x=out_x, y=out_y)
        facet.set_xticks(np.arange(0, grid_size+1,10))
        facet.set_yticks(np.arange(0, grid_size+1,10))
        plt.legend([],[], frameon=False)
        plt.show()
```

![](https://gitlab.dclabra.fi/wiki/uploads/upload_9ecccc13a5b300de55812a26aae3e8c7.png)

### Tilastoja

DataFrameen on haettu kaikki data tietokannasta (13890906 rows × 6 columns)

Datasta on poistettu outlierit Z-Scorella:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_dd65d47842690692cd8862caeef46118.png)

Datasta on poistettu aukioloaikojen ulkpuoliset rivit, jonka jälkeen dataa on:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_af453b5934fa00562e83feaeaf6847e6.png)

Reittien erottelun ja alle 50 riviä sisältävien reittien poistamisen jälkeen dataa on jäljellä:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_09c4c70373a20b0213ef094936316eba.png)

![](https://gitlab.dclabra.fi/wiki/uploads/upload_6f877d1f108628e529acaef7f750200b.png)

Reittien erotteluun kului aikaa:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_6b3ef2cf908213a21c5289069dfd22c8.png)

Eroteltuja kauppareissuja löytyi: 8788 kpl
Datan Siivous - Nopeuksien Siivous
=

***(Huom. esimerkissä dataa on käsittelyssä 1 000 000 pistettä)***

Kun datasta on poistettu selvät outlierit, on silti jäljellä muutamia outouksia, esim epärealistisen nopeasti liikkuvia pisteitä.

Nämä nopeudet voivat olla hyppyjä, jossa paikka on vaihtunut sekunnissa toiselle puolelle kauppaa.

Eli algorytmi etsii tälläiset pisteet ja poistaa ne.

# Algorytmin käyttäminen

Algorytmi on luokka nimeltään "velocity", jolla voidaan sitten käyttää funktioita "column_vel" ja "draw_vel".
```python
# Importointi
from clean_velocities import *
```

Käyttö
```python
# Otetaan kopio taulusta piirtämistä varten
dftest = df1.copy()
# Laskee x:n ja y:n oudot nopeudet
uusi_df = velocity.column_vel(df1, 'x', 'y')
# Piirtää kuvan näistä
velocity.draw_vel(dftest, df1, 'x', 'y')

# Katsotaan näkyykö uudet "velocity" ja "distance" kolumnit
uusi_df.head()
```

Ulostulo
```python
Uusi taulu:  40582
Poistettuja pisteitä:  50
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_16af4a7b11cb7be5a0f7597d499c1af3.png)

---

# Vanha clean_velocities funktio

Kuva kertoo enemmän kuin tuhat sanaa ja koodi on kommentoitu.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_3d2af79897d4542ce54a3b54861309d5.png)

Tämän poiston **kriteeri** on kahden eri pisteen nopeuden ja kuljetun matkan suuruus, jonka pitää olla alle tiettyjen arvojen.

```python
import numpy as np
import math
import matplotlib.pyplot as plt


class velocity():
    """[Luokalla "velocity" on 4 funktiota: calc_timejump, calculateDistance, column_vel & draw_vel]
    """
    # Nopeuden laskun funktio
    def calc_timejump(time_start, time_end):
        """[Laskee kuinka paljon aikaa on kulunut lähdetystä timestampista toiseen.]

        Args:
            time_start ([timestamp]): [Timestamp, mistä lähdetään liikkelle]
            time_end ([timestamp]): [Timestamp, mihin päädytään] 
        """
        # Lasketaan aloitus- ja lopetusajan erotus
        diff_time = np.datetime64(time_start) - np.datetime64(time_end)
        # Palauttaa sekuntien kokonaismäärän
        # Tosin palauttaa microsekunneksi
        diff_time.item().total_seconds()
        # Muuttaa sekunneiksi
        diff_time = diff_time / np.timedelta64(1, 's')

        # Pudottaa jo tässä vaiheessa tosi pienet ajat
        if(diff_time > 0.1):
            return diff_time
        else:
            return 0.1
        
    def calculateDistance(x1, y1, x2, y2): 
        """[Laskee euklidisen normin sqrt(x * x + y * y) Tämä on vektorin pituus origosta pisteeseen]

        Args:
            x1 ([int]): [x kolumnin arvo, jota käsitellään]
            x2 ([int]): [x kolumnin arvo seuraavana x1:sestä]
            y1 ([int]): [y kolumnin arvo, jota käsitellään]
            y2 ([int]): [y kolumnin arvo seuraavana y1:sestä]
            
        Returns:
            [float]: [Palauttaa euclidisen pituuden datapisteiden välillä]
        """
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return dist

    def column_vel(df, x_sarake, y_sarake):
        """[Laskee datapisteiden välisen nopeuden]

        Args:
            df ([DataFrame]): [Taulu, jota halutaan käsitellä. Vaatii sarakkeet 'x', 'y' & 'timestamp']
            x_sarake ([string]): [Sarake, missä x koordinaatit]
            y_sarake ([string]): [Sarake, missä y koordinaatit]
            
        Returns:
            mergedDf ([DataFrame]): [Alkuperäinen syötetty taulu, johon on lisätty 'velocity' ja 'distance' sarakkeet]
        """
        # Alustaa muuttujia
        df_original = df.copy()
        devx1 = []
        time = []
        dist = []
        speed = []
        # x ja y kolumnin indexi
        x_column = df.columns.get_loc(x_sarake)
        y_column = df.columns.get_loc(y_sarake)
        # timestampin indexi
        time_column = df.columns.get_loc('timestamp')
        i = 1
```

Nyt siis iteroidaan taulukon läpi, otetaan piste ja sitä seuraava ja lasketaan niiden välinen nopeus ja kuljettu matka (Matka on siis pisteinä: 1 = 1 piste kuljettu)
```python
        # Iteroidaan taulukon pituuden läpi
        for i in range(len(df[x_sarake])):
            # Ottaa timestamp kolumnista yhden ja sitä seuraavan arvon ja laskee niiden välisen nopeuden
            time.append(velocity.calc_timejump(df.iloc[i, time_column], df.iloc[i+1, time_column]))
            # Sama kuin ylemmässä, mutta lisätään iteroitavan y kolumnin mukaan ja laskeetaan niiden välisen pituuden
            dist.append(velocity.calculateDistance(abs(df.iloc[i, x_column]), abs(df.iloc[i, y_column]),abs(df.iloc[i+1, x_column]), abs(df.iloc[i+1, y_column])))
```

Lasketaan pisteiden välinen nopeus simppelillä fysiikalla: **Matka jaettuna ajalla**
```python
        # Lasketaan nopeus jakamalla pituus nopeudella
        for i in range(len(dist)):
            speed.append((dist[i] / 93) / time[i])
            #speed.append((dist[i] / 93)/time[i])

        x = 0
```

Filtteröidään nyt liian suuret nopeudet ja kuljetut matkat pois:

Kriteerit ovat seuraavanlaiset:
- Jos nopeus on yli 2 km/h
- Jos kuljettu matka on yli 100 pistettä

Yksi node ei vain järkevästi voisi liikkua puolessa sekunnissa yli 100 pistettä vain 2 km/h tunti vauhtia.
```python
        # Poistetaan liiat nopeudet joko:
        # jos nopeus on liian suuri (yli 2 km/h)
        # jos on kulkenut liian pitkän matkan liian nopeasti (jos yli 100 pistettä)
        for i in speed:
            if(i > 2 or (dist[x]/93) > 100):
                df.drop([df.index[x]], axis = 0, inplace = True)
                x -= 1
            x += 1
```

# Uusi clean_velocities funktio
HUOM: Koska kaikki tuo ylempi koodi onkin aivan liian hidas, muutettiin koodia huomattavasti optimaallisimmaksi:
```python
def clean_vel(df, x_sarake, y_sarake):

        df_original = df.copy()
        # Laskee differentiaalin rivien välillä
        df['distancex'] = df[x_sarake].diff()
        df['distancey'] = df[y_sarake].diff()

        # Laskee euklidisen normin sqrt(x * x + y * y) Tämä on vektorin pituus origosta pisteeseen
        df['distance'] = (df['distancex']**2 + df['distancey']**2)
        df['distance'] = (np.sqrt(df['distance'])/100)
        np.sqrt(df['distance'])/100

        # Pudottaa temp sarakkeet
        df = df.drop('distancex', 1)
        df = df.drop('distancey', 1)

        # laskee timestamppien differences
        df['ero'] = df['timestamp'].diff()
        df['ero'] = df.ero.dt.seconds                   
        # Laskee nopeuden
        df['speed_kmh'] = df['distance']/df['ero']*3.6


        # Poistetaan liian nopeat, yli 7km/h
        df = df.dropna()
        print(df)
        
        df = df[df['speed_kmh'] < 7.0]
        df = df[df['distance'] < 100]

        print("Vanha taulu: ", len(df_original))
        print("Uusi taulu: ", len(df['x'])) 
        print("Poistettuja pisteitä: ", len(df_original) - len(df))
        total_data = len(df_original)
        total_missing = len(df_original) - len(df)
        percentage = (total_missing/total_data) * 100
        percentage_remain = (1 - (total_missing/total_data)) * 100
        print("Percent removed:   ",round(percentage, 2),'%')
        print("Percent remaining: ",round(percentage_remain, 2),'%')
        print(f"{'-'*30}")
```

Tulostetaan poistettujen pisteiden määrä ja luodaan syötettyyn tauluu uudet sarakkeet:
- Velocity
- Distance

Oikein hyödylliset piirteet, jotka kannattaa ottaa talteen.
```python
        print("Uusi taulu: ", len(df['x'])) 
        print("Poistettuja pisteitä: ", len(df_original) - len(df))
        
        # Luodaan taulu nopeuksista ja pituuksista
        new_df = pd.DataFrame(list(zip(speed, dist)),columns=['velocity', 'distance'])
        
        # Yhdistetään tämä taulu syötettyyn tauluun
        mergedDf = df.join(new_df)
        mergedDf
        
        return mergedDf
```

# Kuvaaja
Kuvaajan piirto on yksinkertainen:

```python
def draw_vel(df_original, df_new, columnX, columnY):
        """[Piirtää kuvaajan poistetuista (Musta) ja jääneistä (Cyan) pisteistä]

        Args:
            df_original ([DataFrame]): [Taulu ennen siivousta]
            df_new ([DataFrame]): [Taulu siivouksien jälkeen]
            columnX ([string]): [Koordinaattien x sarake]
            columnY ([string]): [Koordinaattien y sarake]
        """
        plt.figure(figsize=(10, 7))
        plt.plot(df_original[columnX], df_original[columnY], color="black", marker='o', linestyle='dashed', linewidth=0.2, markersize=3, label="Poistettu")
        plt.plot(df_new[columnX], df_new[columnY],color='cyan', marker='o',linewidth=0.2, markersize=2, markevery=3, label="Jääneet", alpha=0.3)
        plt.title("Liiat nopeudet poistettu")
        plt.legend()
        plt.show()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_0d83d60eaadf85e61b82b3d69647ae26.png)
```
Aika:  2:12:09.744104
Alkuperäinen data: 809329 # HUOM. Tässä oli jo pudotettu aukioloaikojen ulkopuolella olevat pisteet.
Poistettuja pisteitä:  123420
```

---
# Konkluusio
Vanha algorytmi on siis **TOSI** hidas. **Miljoonalla** datapisteellä, sillä kesti **2 TUNTIA** käydä data läpi ja siivota se.

**Uusi algorytmi** on PALJON nopeampi

Loppujen lopuksi näyttää toimineen: Epärealistisia nopeuksia oli 16% datasta ja suurin osa näyttääkin olevan oletettavien "seinien" ja hyllyjen ulkopuolelle ja yli hyppineet pisteet.

Tätä voi siis käyttää, mutta vasta kun käsittelee ***pienempää*** datasettiä, esim ***yksittäistä reittiä.***
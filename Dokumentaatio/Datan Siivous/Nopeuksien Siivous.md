Datan Siivous - Nopeuksien Siivous
=

***(Huom. esimerkissä dataa on käsittelyssä 1 000 000 pistettä)***

Kun datasta on poistettu selvät outlierit, on silti jäljellä muutamia outouksia, esim epärealistisia nopeuksia.

Nämä nopeudet voivat olla hyppyjä, jossa paikka on vaihtunut sekunnissa toiselle puolelle kauppaa.

Eli algorytmi etsii tälläiset pisteet ja poistaa ne.

# Algorytmin käyttäminen

Algorytmi on luokka nimeltään "velocity", jolla voidaan sitten käyttää funktioita "column_vel" ja "draw_vel".
```python=
# Importointi
from clean_velocities import *

# Tämä on vain funktion käyttämään aikaan
start=datetime.now()

# Otetaan talteen alkuperäinen data vertailua varten
dftest = df1.copy()
table_alkuperäinen = len(df1['x'])

# Laskee x:n ja y:n oudot nopeudet
velocity.column_vel(df1, 'x')
velocity.column_vel(df1, 'y')
# Piirtää kuvan näistä
velocity.draw_vel(dftest, df1, 'x', 'y')

print("Aika: ",datetime.now()-start)
print("Alkuperäinen data: ", len(df1['x']))
print("Poistettuja pisteitä: ", table_alkuperäinen - len(df1['x']))
```

# clean_velocities funktio

Kuva kertoo enemmän kuin tuhat sanaa ja koodi on kommentoitu.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_3d2af79897d4542ce54a3b54861309d5.png)

Tämän poiston **kriteeri** on kahden eri pisteen absoluuttisten arvojen suuruus, jonka pitää olla alle tiettyjen arvojen (tässä tilanteessa 60 ja 100) &larr; *(Nämä arvot ovat siis sekunteja)*

```python
import numpy as np
import math
import matplotlib.pyplot as plt


class velocity():
    # Nopeuden laskun funktio
    def calc_velocity(self, time_start, time_end):
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
        
    def calculateDistance(self, x1, y1, x2, y2):  
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return dist

    def column_vel(df, x_sarake, y_sarake):
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

        # Iteroidaan taulukon pituuden läpi
        for i in range(len(df[x_sarake])):
            # Ottaa timestamp kolumnista yhden ja sitä seuraavan arvon ja laskee niiden välisen nopeuden
            time.append(velocity.calc_velocity(df.iloc[i, time_column], df.iloc[i-1, time_column]))
            # Sama kuin ylemmässä, mutta lisätään iteroitavan y kolumnin mukaan ja laskeetaan niiden välisen pituuden
            dist.append(velocity.calculateDistance(abs(df.iloc[i, x_column]), abs(df.iloc[i, y_column]),abs(df.iloc[i-1, x_column]), abs(df.iloc[i-1, y_column])))
        
        # Tyhjennetään "speed" lista
        speed = []
        # Lasketaan nopeus jakamalla pituus nopeudella
        for i in range(len(dist)):
            speed.append((dist[i] / 93)/time[i])

        x = 0
        # Postetaan liiat nopeudet joko:
        # jos nopeus on liian suuri (yli 2)
        # jos on kulkenut liian pitkän matkan liian nopeasti (jos yli 100 pistettä)
        for i in speed:
            if(i > 2 or (dist[x]/93) > 100):
                df.drop([df.index[x]], axis = 0, inplace = True)
                x -= 1
            x += 1

        print("Uusi taulu: ", len(df['x'])) 
        print("Poistettuja pisteitä: ", len(df_original) - len(df))
```

# Kuvaaja
Kuvaajan piirto on yksinkertainen:

```python
def draw_vel(df_original, df_new, columnX, columnY):
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
# Konkluusio
Algorytmi on siis **TOSI** hidas. **Miljoonalla** datapisteellä, sillä kesti **2 TUNTIA** käydä data läpi ja siivota se.

Loppujen lopuksi näyttää toimineen: Epärealistisia nopeuksia oli 16% datasta ja suurin osa näyttääkin olevan oletettavien "seinien" ja hyllyjen ulkopuolelle ja yli hyppineet pisteet.

Tätä voi siis käyttää, mutta vasta kun käsittelee ***pienempää*** datasettiä, esim ***yksittäistä reittiä.***
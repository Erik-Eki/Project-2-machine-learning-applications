import numpy as np
import pandas as pd
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

        # Iteroidaan taulukon pituuden läpi
        for i in range(len(df[x_sarake])):
            # Ottaa timestamp kolumnista yhden ja sitä seuraavan arvon ja laskee niiden välisen nopeuden
            time.append(velocity.calc_timejump(df.iloc[i, time_column], df.iloc[i-1, time_column]))
            # Sama kuin ylemmässä, mutta lisätään iteroitavan y kolumnin mukaan ja laskeetaan niiden välisen pituuden
            dist.append(velocity.calculateDistance(abs(df.iloc[i, x_column]), abs(df.iloc[i, y_column]),abs(df.iloc[i-1, x_column]), abs(df.iloc[i-1, y_column])))

        # Lasketaan nopeus jakamalla pituus nopeudella
        for i in range(len(dist)):
            speed.append((dist[i] / 93) / time[i])
            #speed.append((dist[i] / 93)/time[i])

        x = 0
        
        # Poistetaan liiat nopeudet joko:
        # jos nopeus on liian suuri (yli 2 km/h)
        # jos on kulkenut liian pitkän matkan liian nopeasti (jos yli 100 pistettä)
        for i in speed:
            if(i > 2 or (dist[x]/93) > 100):
                df.drop([df.index[x]], axis = 0, inplace = True)
                x -= 1
            x += 1

        print("Uusi taulu: ", len(df['x'])) 
        print("Poistettuja pisteitä: ", len(df_original) - len(df))
        
        # Luodaan taulu nopeuksista ja pituuksista
        new_df = pd.DataFrame(list(zip(speed, dist)),columns=['velocity', 'distance'])
        
        # Yhdistetään tämä taulu syötettyyn tauluun
        mergedDf = df.join(new_df)
        mergedDf
        
        return mergedDf


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
        plt.ylabel("y", rotation='0')
        plt.xlabel("x")
        plt.grid()
        plt.title("Liiat nopeudet poistettu")
        plt.legend()
        plt.show()
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from collections import Counter


class velocity():
    def clean_vel(df, x_sarake, y_sarake):
        df_original = df.copy()
        df['distancex'] = df[x_sarake].diff()
        df['distancey'] = df[y_sarake].diff()
        df['distance'] = (df['distancex']**2 + df['distancey']**2)
        df['distance'] = (np.sqrt(df['distance'])/100)
        
        
        
        
        np.sqrt(df['distance'])/100

        
        
        
        df = df.drop('distancex', 1)
        df = df.drop('distancey', 1)


        df['ero'] = df['timestamp'].diff()
        df['ero'] = df.ero.dt.seconds                   

        df['speed_kmh'] = df['distance']/df['ero']*3.6


        # Poistetaan liian nopeat, yli 7km/h
        df = df.dropna()
        print(df)
        
        df = df[df['speed_kmh'] < 7.0]
        df = df[df['distance'] < 100]
        
        # Poistetaan liiat nopeudet joko:
        # jos nopeus on liian suuri (yli 2 km/h)
        # jos on kulkenut liian pitkän matkan liian nopeasti (jos yli 100 pistettä)
        '''speed = df['speedkm'].values
        dist = df['distance'].values
        x = 0
        for i in speed:
            if(i > 5.0 or (dist[x]/100) > 100):
                df.drop([df.index[x]], axis = 0, inplace = True)
                x -= 1
            x += 1
        '''
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
        # Luodaan taulu nopeuksista ja pituuksista
        #s = pd.Series(dist)
        #s = (s / 100).tolist()
        #new_df = pd.DataFrame(list(zip(speed, s)),columns=['velocity_kmh', 'distance_m'])
        
        # Yhdistetään tämä taulu syötettyyn tauluun
        #mergedDf = df.join(new_df)
        #mergedDf
        
        return df

    '''
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
            dist.append(round(velocity.calculateDistance(abs(df.iloc[i, x_column]), abs(df.iloc[i, y_column]),abs(df.iloc[i-1, x_column]), abs(df.iloc[i-1, y_column])),1))

        # Lasketaan nopeus jakamalla pituus ajalla
        for i in range(len(dist)):
            speed.append((dist[i] / 100) / time[i])
            #speed.append((dist[i] / 93)/time[i])
        speed2 = speed
        dist2 = dist    
        
        x = 0'''
    
    def column_vel_GRID(df, x_sarake, y_sarake, speed2, dist2):
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
            dist.append(round(velocity.calculateDistance(abs(df.iloc[i, x_column]), abs(df.iloc[i, y_column]),abs(df.iloc[i-1, x_column]), abs(df.iloc[i-1, y_column])),1))

        # Lasketaan nopeus jakamalla pituus ajalla
        for i in range(len(dist)):
            speed.append((dist[i]) / time[i])
            #speed.append((dist[i] / 93)/time[i])
        #print([speed.count(x) for x in set(speed)])
        #print(Counter(speed))
        speed = speed2
        dist = dist2
        
        x = 0
        # Poistetaan liiat nopeudet joko:
        # jos nopeus on liian suuri (yli 2 km/h)
        # jos on kulkenut liian pitkän matkan liian nopeasti (jos yli 100 pistettä)
        '''for i in speed:
            #print(x)
            if(i > 5.0 or dist[x] > 10.0):
                df['Deleted']=df.index[x]==True
                df.drop([df.index[x]], axis=0, inplace = True)
                #print("Piste poistettud")
                x -= 1
            else:
                df['Deleted']=df.index[x]==False
                x -= 1
            x += 1'''
        for i in speed:
            if(i > 5.0 or dist[x] > 10):
                df.drop([df.index[x]], axis = 0, inplace = True)
                x -= 1
            x += 1
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
        
        # Luodaan taulu nopeuksista ja pituuksista
        new_df = pd.DataFrame(list(zip(speed, dist)),columns=['velocity_kmh', 'distance_m'])
        
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
        plt.plot(df_new[columnX], df_new[columnY],color='cyan', markeredgecolor='deeppink', marker='o',linewidth=0.2, markersize=4, markevery=3, label="Jääneet")
        plt.ylabel("y", rotation='0')
        plt.xlabel("x")
        plt.grid()
        plt.title("Liiat nopeudet poistettu")
        plt.legend()
        plt.show()

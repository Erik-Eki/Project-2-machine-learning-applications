import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

class velocity():
    # Nopeuden laskun funktio
    def calc_velocity(time_start, time_end):
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

    def x_vel(df):
        # Alustaa muuttujia
        prev = 0
        val = 0
        x = 0
        # x kolumnin indexi
        column = df.columns.get_loc('x')
        # timestampin indexi
        time_column = df.columns.get_loc('timestamp')
        # Iteroidaan taulukon pituuden läpi...
        for i in range(len(df['x'])):
            # ...Niin pitkään kunnes päästään loppuun
            if(i < len(df['x'])):
                # Ottaa timestamp kolumnista yhden ja sitä seuraavan arvon ja laskee niiden välisen nopeuden
                value1 = calc_velocity(df.iloc[i-x, time_column], df.iloc[i-(1+x), time_column])
                # Lasketaan absoluuttinen arvo ja vähennetään siitä edellisen nopeuden absoluuttinen arvo
                value2 = int((abs(df.iloc[i-x, column])) - prev)
                # Laskee näiden osamäärän
                val =  value2 / value1

                # Jos nopeus on liian suuri, pudottaa sen
                if (val > 60 or value2 > 100):
                    df1.drop([df.index[i-x]], axis = 0, inplace = True)
                    prev = abs(df.iloc[i-x, column])
                    x +=1
                else:
                    prev = abs(df.iloc[i-x, column])

    def y_vel(df):
        prev = 0
        val = 0
        x = 0
        column = df.columns.get_loc('y')
        time_column = df.columns.get_loc('timestamp')
        for i in range(len(df['y'])):

            if(i < len(df['y'])):

                value1 = calc_velocity(df.iloc[i-x, time_column], df.iloc[i-(1+x), time_column])
                value2 = int((abs(df.iloc[i-x, column]))-prev)
                val = value2 / value1

                if (val > 60 or value2 > 100):
                    df.drop([df.index[i-x]], axis = 0, inplace = True)
                    prev = abs(df.iloc[i-x , column])
                    x +=1
                else:
                    prev = abs(df.iloc[i-x, column])


    def draw_vel():
        plt.figure(figsize=(10, 7))
        plt.plot(df_original['x_grid'], df_original['y_grid'], color="black", marker='o', linestyle='dashed', linewidth=0.2, markersize=3, label="Poistettu")
        #plt.plot(df1['x'], df1['y'], color="cyan", marker='o', linestyle='dashed', outline="r" linewidth=0.2, markersize=3, alpha=0.2, label="Poistettud")
        plt.plot(df_new['x_grid'], df_new['y_grid'],color='cyan', marker='o',linewidth=0.2, markersize=2, markevery=3, label="Jääneet", alpha=0.3)
        plt.title("Liiat nopeudet poistettu")
        plt.legend()
        plt.show()
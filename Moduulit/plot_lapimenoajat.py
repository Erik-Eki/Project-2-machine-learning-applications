import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_lapimeno(aloitukset, lapimenoajat):

    df2 = pd.DataFrame(list(zip(aloitukset,lapimenoajat)), columns =['Aloitus', 'Kesto'])
    df2['h'] = df2['Aloitus'].dt.strftime('%H').astype('float')
    df2_aika = [8, 11, 13, 15, 17, 19, 21]
    df2_ajat = pd.cut(df2['h'], df2_aika)  #Tehdään ajat bin johon tallennetaan tunnit ja näin pystyy laittamaan läpimenoajat eri tunti-ikkunoitten sisään
    keskiarvot = (df2.groupby (df2_ajat)["Kesto"].count() / len(df2['Kesto'])) * 60 #Lasketaan keskiarvot aikaikkunoitten sisällä sekä muutetaan saadut luvut minuuteiksi
    keskiarvot=(round(keskiarvot)) #Pyöristetään saadut luvut


    plot_df_keskiarvo = (keskiarvot)
    plt.ylabel("min")
    plt.title("Läpimenoaikojen keskiarvot tiettyihin kellonaikohin")
    plot_df_keskiarvo.plot(kind = 'bar')
    plt.show()


    df2['viikonpäivä'] = df2['Aloitus'].apply(lambda x: x.weekday())
    df2['viikonpäivä'] = df2['Aloitus'].dt.day_name()
    sorter = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df2['viikonpäivä'] = pd.Categorical(df2['viikonpäivä'], categories=sorter, ordered=True)
    df2 = df2.sort_values('viikonpäivä')

    päivät = df2['viikonpäivä']
    keskiarvot_pv = (df2.groupby (päivät)["Kesto"].count() / len(df2['Kesto'])) * 60
    keskiarvot_pv=(round(keskiarvot_pv))

    plot_df_keskiarvo_pv = (keskiarvot_pv)
    plt.ylabel("min")
    plt.title("Läpimenoaikojen keskiarvot tiettyinä päivinä")
    plot_df_keskiarvo_pv.plot(kind = 'bar')
    plt.show()
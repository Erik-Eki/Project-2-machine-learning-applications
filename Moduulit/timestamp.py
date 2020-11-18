import pandas as pd


def aukioloajat(df):
    
    df = df.drop(df[(df.timestamp.dt.hour < 8)].index) #dropataan kaikki 8-21 ulkopuolella olevat tunnit
    df = df.drop(df[(df.timestamp.dt.hour > 21)].index)
    df = df.reset_index() # resetoidaan indexit, että voidaan ajaa uudet koodit
    
    df_temp = df[df.timestamp.dt.dayofweek == 6].index.values.tolist()
    df_new_temp = df.iloc[df_temp][df.iloc[df_temp].timestamp.dt.hour < 10] # # Suodatetaan kaikkien 6 päivän indekseistä alle 10 tuntiset
    df = df.drop(df.index[df_new_temp.index.values])     # Poistetaan alkuperäisestä dataframesta kyseiset arvot
    #df_temp = df[df.timestamp.dt.day == ].index.values.tolist()
    #df = df.drop(df.loc[((df.timestamp.dt.day == 25) & (df.timestamp.dt.month == 5) & (df.timestamp.dt.hour < 10))].index.tolist()
    return df
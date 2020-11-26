import pandas as pd

def clean_dataframe(df):
    
    # node_id:s to 1-32 format
    df['node_id'] = pd.factorize(df['node_id'])[0] + 1
    
    # Timestamp to datetime
    df['timestamp'] = df['timestamp'].astype(str)
    df['timestamp'] = df['timestamp'].str.slice(2, -7)
    df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
    
    # Round ms
    df.timestamp = df.timestamp.dt.round("ms")
    df.timestamp = df.timestamp.dt.tz_localize('UTC')

    # Muunnetaan Suomen aikaan. Tämä huomioi kesä- ja talviajan.
    df.timestamp = df.timestamp.dt.tz_convert('Europe/Helsinki')
    
    # Drop +00 ending
    df['timestamp'] = df['timestamp'].astype(str)
    df['timestamp'] = df['timestamp'].str.slice(0, -7)
    df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
    
    # viikonpäiväkolumni
    df['dayofweek'] = df.timestamp.dt.dayofweek
    
    

    
    # Poistetaan aukioloaikojen ulkopuolella olevat ajat
    df = df.drop(df[(df.timestamp.dt.hour < 8)].index) #dropataan kaikki 8-21 ulkopuolella olevat tunnit
    df = df.drop(df[(df.timestamp.dt.hour > 21)].index)
    df = df.reset_index(drop=True) # resetoidaan indexit, että voidaan ajaa uudet koodit
    
        #alustetaan uusi kolumni nollalla, tähän tulee kyseinen tunti kaupassa, esimerkiksi klo 8 eli aukioloajan ensimmäinen tunti on 1
    df['current_hour'] = 0
    # Käydään läpi timestamp ja jokaikisen tunnin kohdalle lisätään yksi tunti. Aloitetaan tunnista 8
    #Koska 8-21 välillä 15 tuntia, ajetaan tämä 15 kertaa
    for i in range(15):
        
        
        df['current_hour'].loc[df['timestamp'].dt.hour == 8+i] = i+1

    #Sunnuntaina aloitetaan kaksi tuntia myöhemmin, joten vähennetään kaksi tuntia jokaisesta hetkestä
    df['current_hour'].loc[df['timestamp'].dt.dayofweek == 6] = df['current_hour'].loc[df['timestamp'].dt.dayofweek == 6] - 2
    
    # Suodatetaan Sunnuntaitten aukioloajat
    df_temp = df[df.timestamp.dt.dayofweek == 6].index.values.tolist()
    df_new_temp = df.iloc[df_temp][df.iloc[df_temp].timestamp.dt.hour < 10] #

    # Poistetaan alkuperäisestä dataframesta kyseiset arvot
    df = df.drop(df.index[df_new_temp.index.values])
    
    df = df.reset_index(drop=True)
    
    # Drop z and q columns
    df = df.drop(columns=['z','q'])
    
    return df

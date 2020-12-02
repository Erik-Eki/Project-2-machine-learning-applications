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
    
    print(df.timestamp.dt.hour.unique())
    print(f"{'-'*30}\nFiltering out after-hours\n")
    print("Data before filtering: ", len(df))
    print("Deleted nodes before 8:00: ",len(df) - len(df.drop(df[(df.timestamp.dt.hour < 8)].index)))
    print("Deleted nodes after 21:00: ", len(df) - len(df.drop(df[(df.timestamp.dt.hour > 21)].index)))
    print("Deleted after-hours nodes: ", (len(df.drop(df[(df.timestamp.dt.hour < 8)].index)) + len(df.drop(df[(df.timestamp.dt.hour > 21)].index))))
    # Poistetaan aukioloaikojen ulkopuolella olevat ajat
    df = df.drop(df[(df.timestamp.dt.hour < 8)].index) #dropataan kaikki 8-21 ulkopuolella olevat tunnit
    df = df.drop(df[(df.timestamp.dt.hour > 21)].index)
    df = df.reset_index(drop=True) # resetoidaan indexit, että voidaan ajaa uudet koodit
    
    # alustetaan uusi kolumni nollalla, tähän tulee kyseinen tunti kaupassa, esimerkiksi klo 8 eli aukioloajan ensimmäinen tunti on 1
    df['current_hour'] = 0
    
    # Käydään läpi timestamp ja jokaikisen tunnin kohdalle lisätään yksi tunti. Aloitetaan tunnista 8
    #Koska 8-21 välillä 15 tuntia, ajetaan tämä 15 kertaa
    for i in range(15):
        df['current_hour'].loc[df['timestamp'].dt.hour == 8+i] = i+1

    #Sunnuntaina aloitetaan kaksi tuntia myöhemmin, joten vähennetään kaksi tuntia jokaisesta hetkestä
    df['current_hour'].loc[df['timestamp'].dt.dayofweek == 6] = df['current_hour'].loc[df['timestamp'].dt.dayofweek == 6] - 2
    
    # Suodatetaan Sunnuntaitten aukioloajat
    df_temp = df[df.timestamp.dt.dayofweek == 6].index.values.tolist()
    df_new_temp = df.iloc[df_temp][df.iloc[df_temp].timestamp.dt.hour < 10]

    # Poistetaan alkuperäisestä dataframesta kyseiset arvot
    df = df.drop(df.index[df_new_temp.index.values])
    
    df = df.reset_index(drop=True)
    
    # Drop z and q columns
    df = df.drop(columns=['z','q'])
    
    bad_nodes = [13,14,18,27,32]
    
    # Poistetaan huonot nodet
    print(f"{'-'*30}\nBad nodes: {bad_nodes}\n")
    print("Amount of bad nodes", (len(df[df.node_id == 13]) + len(df[df.node_id == 14]) + len(df[df.node_id == 18]) + len(df[df.node_id == 27]) + len(df[df.node_id == 32])))
    print("Data after deleting bad nodes: ", len(df) - (len(df[df.node_id == 13]) + len(df[df.node_id == 14]) + len(df[df.node_id == 18]) + len(df[df.node_id == 27]) + len(df[df.node_id == 32])))
    print(f"{'-'*30}")
    
    df = df[df.node_id != 13]
    df = df[df.node_id != 14]
    df = df[df.node_id != 18]
    df = df[df.node_id != 27]
    df = df[df.node_id != 32]
    
    return df

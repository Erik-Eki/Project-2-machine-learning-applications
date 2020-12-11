import pandas as pd
import numpy as np

def nopeudet(df):
    
    df_original = df.copy()
    df['distancex'] = df['x'].diff()
    df['distancey'] = df['y'].diff()
    df['distance'] = (df['distancex']**2 + df['distancey']**2)
    df['distance'] = (np.sqrt(df['distance'])/100)

    df = df.drop('distancex', 1)
    df = df.drop('distancey', 1)


    df['ero'] = df['timestamp'].diff()
    df['ero'] = df.ero.dt.seconds                   
                   
    df['speedkm'] = df['distance']/df['ero']*3.6


    # Poistetaan liian nopeat, yli 7km/h
    
    df = df.dropna()
    
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
    
    return df
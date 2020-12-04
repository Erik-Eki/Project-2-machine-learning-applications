import pandas as pd
import numpy as np

def nopeudet(df):
    

    df['distancex'] = df['x'].diff()
    df['distancey'] = df['y'].diff()
    df['distance'] = (df['distancex']**2 + df['distancey']**2)
    df['distance'] = (np.sqrt(df['distance'])/100)

    df = df.drop('distancex', 1)
    df = df.drop('distancey', 1)


#df['distance'] = ((np.sqrt((df['x'] - df['x'].shift(-1))**2 + (df['y'] - df['y'].shift(-1))**2))/161.15)
#df['distance'] = ((np.sqrt((df['x'].diff()**2 + (df['y'].diff()**2))/161.15)))


    df['ero'] = df['timestamp'].diff()
    df['ero'] = df.ero.dt.seconds                   
                   
    df['speedkm'] = df['distance']/df['ero']*3.6


    # Poistetaan liian nopeat, yli 7km/h
#     df = df.drop(df[(df.speedkm > 7)].index)
    
    df = df.dropna()
    df
    
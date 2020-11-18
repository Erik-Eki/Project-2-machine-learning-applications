import pandas as pd

def horrostila(df):
    # temp time_delta
    df['time_delta'] = df.timestamp.diff()
    
    # Boolean if timedelta >= 10
    df['Horrostila'] = df.time_delta.dt.seconds >= 10
    
    # drop temp time_delta
    df = df.drop(columns=['time_delta'])
    
    return df
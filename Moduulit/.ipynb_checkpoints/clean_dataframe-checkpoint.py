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

    # Drop z and q columns
    df = df.drop(columns=['z','q'])
    
    return df
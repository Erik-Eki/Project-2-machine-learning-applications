def xy_to_grid(df,x,y,k):
    import pandas as pd
    
    x_cut = pd.cut(df.x, k,labels=False)
    y_cut = pd.cut(df.y, k,labels=False)

    # Laitetaan saadut liukuluvut dataframeen
    df['x_grid'],df['y_grid'] = x_cut.values, y_grid.values
       
    # Laitetaan x ja y str ja sitte + yhteen 
    xy_grid_temp = df['x_grid'].astype(str) + '.' + data['y_grid'].astype(str)

    # Muunnetaan str floatiksi
    xy_grid_temp.astype(float)

    # Laitetaan arvot dataframeen
    df['xy_grid'] = xy_grid_temp.values

    # Poistetaan vanhat x_grid ja y_grid sekä z ja q
    df = df.drop(columns=['x_grid','y_grid'])
    return df
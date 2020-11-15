import pandas as pd
import math

def xy_to_grid(df,x,y,k):
    
    df = df.reset_index(drop=True)
    
    xmin, ymin = df.x.min(), df.y.min()
    xmax, ymax = df.x.max(), df.y.max()
    gridlista_x, gridlista_y = [], []

    for i in range(len(df)):
        gridlista_x.append(math.floor((k-1)*(df.loc[i].x-xmin)/(xmax-xmin)))
        gridlista_y.append(math.floor((k-1)*(df.loc[i].y-ymin)/(ymax-ymin)))

    
    # Laitetaan saadut liukuluvut dataframeen
    df['x_grid'],df['y_grid'] = gridlista_x, gridlista_y

    # Laitetaan arvot dataframeen, xygridiID = y * gridsize +x
    df['grid_id'] = df['y_grid'] * k + df['x_grid']

    df = df.reset_index(drop=True)
    
    return df
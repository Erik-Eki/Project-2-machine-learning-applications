import pandas as pd
import math
def xy_to_grid(df,x,y,k):
    x_cut = pd.cut(df.x, k,labels=False)
    y_cut = pd.cut(df.y, k,labels=False)
    # Laitetaan saadut arvot dataframeen
    df['x_grid'], df['y_grid'] = x_cut.values, y_cut.values
    # Laitetaan arvot dataframeen, xygridiID = y * gridsize +x
    df['grid_id'] = df['y_grid'] * k + df['x_grid']
    return df
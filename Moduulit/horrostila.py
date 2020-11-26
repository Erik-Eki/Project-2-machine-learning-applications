import pandas as pd
import matplotlib.pyplot as plt

def horrostila(df):
    # temp time_delta
    df['time_delta'] = df.timestamp.diff()
    
    # Boolean if timedelta >= 10
    df['Horrostila'] = df.time_delta.dt.seconds >= 10
    
    # drop temp time_delta
    df = df.drop(columns=['time_delta'])
    
    return df

def draw_horrostilat(df, x, y):
    dftest = df[df['Horrostila'] == True]
    print("Alkuperäiset nodet: ",len(df))
    print("Poistetut horrostilassa olevat nodet: ", len(df) - len(dftest))
    print("Horrostilassa olevat nodet: ",len(dftest))
    plt.scatter(df[x], df[y], c='coral', marker='s', s=10, alpha=0.3, label="Normaalit")
    plt.scatter(dftest[x], dftest[y], c='cyan', marker='s', edgecolors="black",  s=10, alpha=0.3, label="Horrostilassa")
    plt.title("Nodejen status")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    plt.show()
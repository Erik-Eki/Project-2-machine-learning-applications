import matplotlib.pyplot as plt
import numpy as np

def draw_nodes(df, column):
    ajot = df[column].unique()
    ajot_len = len(df[column].unique())

    print("Nodes: ",ajot_len)

    Cols = 5

    Rows = ajot_len // Cols 
    Rows += ajot_len % Cols
    
    Position = range(1,ajot_len + 1)
    
    fig = plt.figure(1,figsize=(18,15))

    for i, k in zip(ajot,range(ajot_len)):
        # add every single subplot to the figure with a for loop
        ax = fig.add_subplot(Rows,Cols,Position[k])
        ax.plot(df[df[column] == i]['x'], df[df[column] == i]['y'], color=np.random.random(3))
        ax.set_title(f"{column} {k}")
        ax.set_xticks([min(df[df[column] == i]['x']),0,1000,2000,3000, max(df[df[column] == i]['x'])])
        ax.set_yticks([min(df[df[column] == i]['y']),0,1000,2000,3000, max(df[df[column] == i]['y'])])
    plt.tight_layout()
    plt.savefig('all-nodes-unclean.png')
    plt.show()
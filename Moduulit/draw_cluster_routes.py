import numpy as np
import matplotlib.pyplot as plt

def draw_cluster_route(df, column, hue):
    ajot = df[column].unique()
    print(ajot)
    ajot_len = len(df[column].unique())

    #c = cm.flag(np.linspace(0, 1, ajot_len))

    print("Ajokerrat: ",ajot_len)
    
    Cols = 6

    Rows = ajot_len // Cols 
    Rows += ajot_len % Cols
    
    Position = range(1,ajot_len + 1)
    
    fig = plt.figure(1,figsize=(30,15))#constrained_layout=True
    
    plt.rcParams['figure.facecolor'] = 'black'
    #fig, axes = plt.subplots(nrows=3, ncols=6, figsize=(12, 8))
    for i, k in zip(ajot, range(ajot_len)):
        ax = fig.add_subplot(Rows,Cols,Position[k])
        #plt.subplot(10,6,x+1)
        #sns.color_palette("hls", 8)
        sns.scatterplot(x="x", y="y", data=df[df[column] == i],  hue=hue, markers=False, size=30, legend='full', palette="rainbow", ax=ax)
        #ax.plot(df[df[column] == i]['x'], df[df[column] == i]['y'], c=df['ajokerta'])#np.random.random(3)
        ax.set_title(f"Klusteri: {i}",color="white")
        #ax.set_xticks([])#fontsize=7
        #ax.set_yticks([])
        #ax.set_xlim(min(df['x']),max(df['x']))
        #ax.set_ylim(min(df['y']),max(df['y']))
        ax.grid(color='white', linestyle='--', linewidth=1, alpha=0.5)
        ax.set_facecolor('xkcd:black')
        #ax.autoscale(enable=True)
        ax.legend(loc='lower left',fontsize=8)
        
    plt.suptitle("Kesto & viikonpäivä klusterointi",color="white")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    #plt.savefig('plot-average.pdf')
    #plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
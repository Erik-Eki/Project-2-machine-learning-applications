def draw_route_grid(df, column):
    ajot = df[column].unique()
    ajot_len = len(df[column].unique())

    #c = cm.flag(np.linspace(0, 1, ajot_len))

    print("Nodes: ",ajot_len)
    
    Cols = 6

    Rows = ajot_len // Cols 
    Rows += ajot_len % Cols
    
    Position = range(1,ajot_len + 1)
    
    fig = plt.figure(1,figsize=(12,9))
        
    #fig, axes = plt.subplots(nrows=3, ncols=6, figsize=(12, 8))
    x = 0
    for i, k in zip(ajot,range(ajot_len)):
        # add every single subplot to the figure with a for loop
        ax = fig.add_subplot(Rows,Cols,Position[k])
        #plt.subplot(10,6,x+1)
        ax.plot(df[df[column] == i]['x'], df[df[column] == i]['y'], color=np.random.random(3))#np.random.random(3)
        ax.scatter(in_x, in_y, color='darkorange', marker='s', s=2)
        ax.scatter(out_x, out_y, color='green', marker='s', s=2)
        ax.set_title(f"{column} {i}")
        ax.set_xticks([])#fontsize=7
        ax.set_yticks([])
        ax.set_xlim(0,40)
        ax.set_ylim(0,40)
        #plt.xlim(0, 40)
        #plt.ylim=(0, 40)
        #plt.axis('off')
        x += 1
    plt.tight_layout()
    #plt.savefig('plot-average.pdf')
    plt.show()
import matplotlib.pyplot as plt
from matplotlib import colors

def sisään(df, grid_size):
    min_x = 0.6 * grid_size
    max_x = 0.8 * grid_size
    min_y = 0.25 * grid_size
    max_y = 0.35 * grid_size
    
    sisään_x = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].x_grid
    sisään_y = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].y_grid
    
    return sisään_x, sisään_y

def ulos(df, grid_size):
    min_x = 0.3 * grid_size
    max_x = 0.5 * grid_size
    min_y = 0 * grid_size
    max_y = 0.38 * grid_size
    
    ulos_x = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].x_grid
    ulos_y = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].y_grid
    
    return ulos_x, ulos_y

def draw_exits(df, sisään_x, sisään_y, ulos_x, ulos_y):
    plt.hist2d(df['x_grid'], df['y_grid'], bins = 100, norm = colors.LogNorm())#bins=[np.arange(0,400,5),np.arange(0,300,5)]

    plt.hist2d(sisään_x, sisään_y, bins = 100, norm=colors.LogNorm(),cmap="cool", label="Sisäänkäynti")
    plt.hist2d(ulos_x, ulos_y, bins = 100, norm=colors.LogNorm(),cmap="spring", label="Kassat")
    plt.axis('tight')
    # Loop over data dimensions and create text annotations.
    plt.grid()
    #plt.savefig("Heatmap(bin=100)")
    plt.show()
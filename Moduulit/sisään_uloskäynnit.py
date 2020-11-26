import matplotlib.pyplot as plt
from matplotlib import colors

def sisään(df, x, y):
    grid_size = max(df[x])+1
    min_x = 0.7 * grid_size
    max_x = 0.8 * grid_size
    min_y = 0 * grid_size
    max_y = 0.35 * grid_size
    
    sisään_x = df.loc[df[x]>=min_x].loc[df[x]<=max_x].loc[df[y]>=min_y].loc[df[y]<=max_y][x]
    sisään_y = df.loc[df[x]>=min_x].loc[df[x]<=max_x].loc[df[y]>=min_y].loc[df[y]<=max_y][y]
    
    return sisään_x, sisään_y

def ulos(df, x, y):
    grid_size = max(df[y])+1
    min_x = 0.3 * grid_size
    max_x = 0.55 * grid_size
    min_y = 0.2 * grid_size
    max_y = 0.35 * grid_size
    
    #ulos_x = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].x_grid
    #ulos_y = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].y_grid
    ulos_x = df.loc[df[x]>=min_x].loc[df[x]<=max_x].loc[df[y]>=min_y].loc[df[y]<=max_y][x]
    ulos_y = df.loc[df[x]>=min_x].loc[df[x]<=max_x].loc[df[y]>=min_y].loc[df[y]<=max_y][y]
    
    return ulos_x, ulos_y

def draw_exits(df, sisään_x, sisään_y, ulos_x, ulos_y, x, y):
    plt.hist2d(df[x], df[y], bins = 100, norm = colors.LogNorm())#bins=[np.arange(0,400,5),np.arange(0,300,5)]

    plt.hist2d(sisään_x, sisään_y, bins = 200, norm=colors.LogNorm(),cmap="cool", label="Sisäänkäynti")
    plt.hist2d(ulos_x, ulos_y, bins = 200, norm=colors.LogNorm(),cmap="spring", label="Kassat")
    plt.axis('tight')
    # Loop over data dimensions and create text annotations.
    plt.grid()
    #plt.savefig("Heatmap(bin=100)")
    plt.show()

def xy_to_ID(x,y,grid_size):
    """[Muokkaa annetut x- ja y-koordinaatit ID-muotoon.]

    Args:
        x ([float]): [gridiin sopiva x-koordinaatti]
        y ([float]): [gridiin sopiva y-koordinaatti]
        grid_size ([int]): [Arvo, jonka mukaan gridi on luotu]

    Returns:
        [int]: [Gridin koon mukaan muokattu ID]
    """
    ID = grid_size*y+x
    return ID
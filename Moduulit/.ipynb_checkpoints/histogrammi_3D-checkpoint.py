from mpl_toolkits.mplot3d.axes3d import Axes3D

def draw_3d(df, ID):
    df1 = df[~df[ID].isin(u_in_ID)]
    df1 = df1[~df1[ID].isin(u_out_ID)]

    xAmplitudes = df1.x_grid
    yAmplitudes = df1.y_grid

    x = np.array(xAmplitudes)   #turn x,y data into numpy arrays
    y = np.array(yAmplitudes)

    fig = plt.figure(figsize=(20,10))          #create a canvas, tell matplotlib it's 3d
    ax = fig.add_subplot(111, projection='3d')

    #make histogram stuff - set bins - I choose 20x20 because I have a lot of data
    bins=bins=(50,50)
    hist, xedges, yedges = np.histogram2d(x, y, bins=bins)
    xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])

    xpos = xpos.flatten()/2.
    ypos = ypos.flatten()/2.
    zpos = np.zeros_like (xpos)

    dx = xedges [1] - xedges [0]
    dy = yedges [1] - yedges [0]
    dz = hist.flatten()

    cmap = cm.get_cmap('jet') # Get desired colormap - you can change this!
    max_height = np.max(dz)   # get range of colorbars so we can normalize
    min_height = np.min(dz)
    # scale each z to [0,1], and get their rgb values
    rgba = [cmap((k-min_height)/max_height) for k in dz]

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
    plt.title("3D plottaus tiheyksistä")
    plt.xlabel("y")
    plt.ylabel("x")
    ax.view_init(30,30)
    plt.gca().invert_yaxis()
    plt.show()
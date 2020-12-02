import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
sns.set();

class Reitti:
    """[Objektiin tallennetaan yksittäisen reitin tiedot]
    """
    def __init__(self):
        """[Jokaiselle tallennettavalle tiedolle luodaan oma lista, kun objekti luodaan]
        """
        self.ajokerta = []
        self.node_id = []
        self.timestamp = []
        self.ID = []
        self.x = []
        self.y = []
        self.velocity_kmh = []
        self.distance_grid = []
      

    def lisaa(self,ajokerta, node_id, timestamp, ID, x, y, vel, dist):
        """[Lisätään kerättävät tiedot objektin listoihin.]

        Args:
            ajokerta ([list]): [yksittäisen reitin id]
            node_id ([list]): [yksittäisen reitin node_id]
            timestamp ([list]): [yksittäisen reitin timestampit]
            ID ([list]): [yksittäisen reitin kulkemat ID:t]
            x ([list]): [yksittäisen reitin x-koordinaatit]
            y ([list]): [yksittäisen reitin y-koordinaatit]
        """
        self.ajokerta.append(ajokerta)
        self.node_id.append(node_id)
        self.timestamp.append(timestamp)
        self.ID.append(ID)
        self.x.append(x)
        self.y.append(y)
        self.velocity_kmh.append(vel)
        self.distance_grid.append(dist)


def poista_lyhyet_reitit(reitit, minimi_määrä_dataa):
    """[Poistaa kauppareissut, joissa annettua arvoa pienempi määrä dataa.]

    Args:
        reitit ([list]): [Sisältää kauppareissu-objektit]
        minimi_m ([int]): [Vähittäismäärä datapisteita objektissa.]

    Returns:
        [list]: [Palauttaa listan, jossa tarpeeksi datapisteitä sisältävät kauppareissut.]
    """
    clean_list = []
    shit_list = []
    for i in range(len(reitit)):
        if len(reitit[i].node_id) > minimi_määrä_dataa:
            clean_list.append(reitit[i])
        else:
            shit_list.append(reitit[i])
    print("Poistetut liian lyhyet reitit:", len(set(shit_list)))
    return clean_list


def erottele_reitit(df, in_ID, out_ID):
    """[Iteroi jokaisen dataframen rivin, tutkii milloin uusi kauppareissu alkaa ja lisää reissun tiedot sille luotuun objektiin.]

    Args:
        df ([DataFrame]): [Diskretisoitu dataframe]
        in_ID ([list]): [Sisäänkäyntialueen diskretisoidut koordinaatit ID-muodossa.]
        out_ID ([list]): [Kassa-alueen diskretisoidut koordinaatit ID-muodossa.]

    Returns:
        [list]: [Sisältää yksittäisten reittien objektit.]
    """
    
    # Luodaan dataframeen sarakkeet, joilla seurataan onko rivin paikkakoordinaatit kassa- tai sisäänkäyntialueilla.
    df["IN"] = df["grid_id"].isin(in_ID)
    df["OUT"] = df["grid_id"].isin(out_ID)

    # Näiden avulla seurataan, että useampi peräkkäinen rivi on kassa- tai sisäänkäyntialueilla.
    df['fo_IN'] = df['IN'].shift(5)
    df['fo_OUT'] = df['OUT'].shift(10)

    cleaned_xy = df.copy()
    erotellut_reitit = []      #tähän tallennetaan erotellut kauppareissut
    ajokerta = 0   # pidetään kirjaa kuinka monta kertaa kärry on ajanut kaupan läpi. Käytetään Kärryjen etsimiseen ja erotteluun
    reitti = Reitti()      #luodaan karry
    erotellut_reitit.append(reitti)     #lisätään ensimmäinen karry listaan, koska data alkaa yleensä kesken ajokerran 
    matkalla = False    

    
    for row in df.itertuples():
        
        if matkalla == False and row.IN  == True and row.IN == row.fo_IN:
            # Aloitetaan matka ja luodaan uusi olio kaupparaissulle.
            matkalla = True
            ajokerta += 1
            reitti = Reitti()      
            erotellut_reitit.append(reitti)

        elif row.OUT == True and row.OUT == row.fo_OUT:
            matkalla = False
        
        elif matkalla == True:
            erotellut_reitit[ajokerta].lisaa(ajokerta,row.node_id, row.timestamp,row.grid_id, row.x_grid, row.y_grid, row.velocity_kmh, row.distance_grid)
    
    return erotellut_reitit

def reitit_dataframeksi(reitit):
    """[Luo dataframen, joka sisältää kaikkien kauppareissujen tiedot.]

    Args:
        reitit ([List]): [Sisältää kauppareissu-oliot]

    Returns:
        [DataFrame]: [Palauttaa Dataframen, joka sisältää jokaisen datasta erotellun kauppareissun.]
    """

    kauppareissut = pd.DataFrame()
    reitt = []
    kauppareissut = kauppareissut.append([pd.DataFrame({"ajokerta":a.ajokerta,
                                                        "node_id":a.node_id,
                                                        "timestamp":a.timestamp,
                                                        "x":a.x,
                                                        "y":a.y,
                                                        "grid_id":a.ID,
                                                        "velocity_kmh":a.velocity_kmh,
                                                        "distance_grid":a.distance_grid,
                                                        "kesto":a.timestamp[-1]-a.timestamp[0] }) for a in reitit])
    
    print("Hyvät reitit:", len(kauppareissut['ajokerta'].unique()))
    print(f"{'-'*30}")
    return kauppareissut

def plot_all_routes(df_reitit, grid_size):
    """Plottaa kaikki erotellut reitit samaan kuvaajaan]

    Args:
        df_reitit ([DataFrane]): [Sisältää erotellut reitit]
        grid_size ([int]): [Gridin koko on määritelty arvon mukaan.]
    """
    facet = sns.scatterplot(x="x", y="y", data=df_reitit, hue="ajokerta")
    facet.set_xticks(np.arange(0, grid_size+1,10))
    facet.set_yticks(np.arange(0, grid_size+1,10))
    plt.show()

def plot_unique_routes(df, grid_size, in_x, in_y, out_x, out_y):
    """[Plottaa jokaisen kauppareissun peräkkäin]

     Args:
         df_reitit ([DataFrame]): [Sisältää erotellut kauppareitit]
         grid_size ([int]): [Gridin koko on määritelty tämän mukaan.]
     """
    ajot = df["ajokerta"].unique()
    ajot_len = max(df["ajokerta"].unique())

    #c = cm.flag(np.linspace(0, 1, ajot_len))
    all_colors = [k for k,v in pltc.cnames.items()]

    print("Ajokerrat: ",ajot_len)
    if ajot_len > 10:
        plt.figure(figsize=(20,(ajot_len/2))) # specifying the overall picture size
    elif ajot_len < 10:
        plt.figure(figsize=(20,ajot_len))


    for i in range(ajot_len):
        plt.subplot((ajot_len/5)+1,6,i+1)
        plt.plot(df[df["ajokerta"] == i]['x'], df[df["ajokerta"] == i]['y'], color=np.random.random(3))#np.random.random(3)
        plt.scatter(in_x, in_y, color='darkorange', marker='s', s=2)
        plt.scatter(out_x, out_y, color='green', marker='s', s=2)
        plt.title(f"Ajokerta {i+1}")
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        #plt.xlim(0, 40)
        #plt.ylim=(0, 40)
        #plt.axis('off')

    plt.show()
    '''ajot = df_reitit["ajokerta"].unique()
    df_reitit["color"] = np.arange(0,len(df_reitit),1)
    for ajo in ajot:
        print(len(df_reitit[df_reitit["ajokerta"] == ajo]))

        facet = sns.scatterplot(x="x", y="y", data=df_reitit[df_reitit["ajokerta"] == ajo],  hue="color")
        sns.scatterplot(x=in_x, y=in_y)
        sns.scatterplot(x=out_x, y=out_y)
        facet.set_xticks(np.arange(0, grid_size+1,10))
        facet.set_yticks(np.arange(0, grid_size+1,10))
        plt.legend([],[], frameon=False)
        plt.show()'''
        
def get_lapimeno(reitit, minimi_määrä_dataa):        

    alo = []
    lapimenoajat = [] #Luodaan pari uutta listaa
        

    
    for i in range(len(reitit)):
        if len(reitit[i].node_id) > minimi_määrä_dataa:
            alotus = reitit[i].timestamp[0]
            lopetus = reitit[i].timestamp[-1]
            lapimenoaika = (lopetus - alotus)
            alo.append(alotus)
            lapimenoajat.append(lapimenoaika)  #For looppi missä saadaan luotua läpimenoajat kärryille
    
    
    return alo, lapimenoajat
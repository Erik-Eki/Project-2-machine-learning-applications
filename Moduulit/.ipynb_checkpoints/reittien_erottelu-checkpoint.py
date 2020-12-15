import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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
        self.x = []
        self.y = []
        self.ID = []
        self.weekday = []
        self.hour = []
        self.speed_kmh = []
        self.distance = []
      
        
    def lisaa(self,ajokerta, node_id, timestamp, ID, x, y, weekday, hour, vel, dist):
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
<<<<<<< HEAD
<<<<<<< HEAD
        
    def yhdista_tiedot(self):
        """[Luo Dictionaryn, johon yhdistetään kaikki objektiin tallennettu data.]
        """
        self.tiedot = {"ajokerta": self.ajokerta,
                   "timestamp": self.node_id,
                   "node_id": self.timestamp,
                   "ID": self.ID,
                   "x":self.x,
                   "y":self.y}
=======
=======
        self.weekday.append(weekday)
        self.hour.append(hour)
        self.speed_kmh.append(vel)
        self.distance.append(dist)
>>>>>>> beea667bbf3b3610ca5a22997bc8b4c63b610fb1

>>>>>>> 5aae8586775e71d19e0e5e35aa3c8e8496aeee71

def poista_lyhyet_reitit(reitit, minimi_määrä_dataa):
    """[Poistaa kauppareissut, joissa annettua arvoa pienempi määrä dataa.]

    Args:
        reitit ([list]): [Sisältää kauppareissu-objektit]
        minimi_m ([int]): [Vähittäismäärä datapisteita objektissa.]

    Returns:
        [list]: [Palauttaa listan, jossa tarpeeksi datapisteitä sisältävät kauppareissut.]
    """
    clean_list = []
    for i in range(len(reitit)):
        if len(reitit[i].node_id) > minimi_määrä_dataa:
            clean_list.append(reitit[i])
    return clean_list

<<<<<<< HEAD
def get_lapimeno(reitit, minimi_määrä_dataa):        

    alo = []
    lapimenoajat = [] #Luodaan pari uutta listaa
        

    
    for i in range(len(reitit)):
        if len(reitit[i].timestamp) > minimi_määrä_dataa:
            alotus = reitit[i].node_id[0]
            lopetus = reitit[i].node_id[-1]
            lapimenoaika = (lopetus - alotus)
            alo.append(alotus)
            lapimenoajat.append(lapimenoaika)  #For looppi missä saadaan luotua läpimenoajat kärryille
    
    alotukset = {"Aloitus":alo }
    Lapimenot = {"Lapimenoajat":lapimenoajat}  #Tallennetaan aloitusajat sekä läpimenoajat listoihin
    print("Läpimenoajat", lapimenoajat)


        
def erottele_reitit(df, in_ID, out_ID):
    """[Erottelee yksittäiset reitit annetusta dataframesta. ]

    Args:
        df ([DataFrame]): [Tietokannasta haettu data, josta yksittäiset ajokerrat halutaan erotella.]
        in_ID ([List]): [Sisäänkäynnin x- ja y-koordinaateista muodostettujen ID:iden lista. ]
        out_ID ([List]): [Kassojen x- ja y-koordinaateista muodostettujen ID:iden lista.]

    Returns:
        [List]: [Palauttaa listan objekteja, joista jokainen sisältää yhden kauppareitin tiedot.]
    """
=======
        
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

>>>>>>> 5aae8586775e71d19e0e5e35aa3c8e8496aeee71
    cleaned_xy = df.copy()
    erotellut_reitit = []      #tähän tallennetaan erotellut kauppareissut
    ajokerta = 0   # pidetään kirjaa kuinka monta kertaa kärry on ajanut kaupan läpi. Käytetään Kärryjen etsimiseen ja erotteluun
    reitti = Reitti()      #luodaan karry
    erotellut_reitit.append(reitti)     #lisätään ensimmäinen karry listaan, koska data alkaa yleensä kesken ajokerran 
<<<<<<< HEAD
    matkalla = False
    
    
    for val in range(len(cleaned_xy["grid_id"])-3):
        # Mitataan kahden rivin timestamppien erotusta
        # Luodaan uusi karry-olio, kun kärry/kori saapuu ensimmäisen kerran sisäänkäynnin kohdalle.
                                                                            # Tarkistetaan, että kaksi pistettä peräkkäin on sisäänkäyntialueella 
                                                                            # (yritetään poissulkea signaalivirheestä alueelle tulleet pisteet)
        if cleaned_xy["grid_id"][val] in in_ID and matkalla == False and  cleaned_xy["grid_id"][val+3] in in_ID:
=======
    matkalla = False    

    
    for row in df.itertuples():
        
        if matkalla == False and row.IN  == True and row.IN == row.fo_IN:
            # Aloitetaan matka ja luodaan uusi olio kaupparaissulle.
>>>>>>> 5aae8586775e71d19e0e5e35aa3c8e8496aeee71
            matkalla = True
            ajokerta += 1
            reitti = Reitti()      
            erotellut_reitit.append(reitti)

<<<<<<< HEAD
        # lopetetaan matka, kun kärry saapuu kassoille (tarkistetaan taas, että useampi piste on alueella peräkkäin)
        elif cleaned_xy["grid_id"][val] in out_ID and cleaned_xy["grid_id"][val+3] in out_ID:
            matkalla = False
            
        # Lisätään rivin teidot objektiin, jos kärry on matkalla (tarkistetaan myös, ettei kesken matkaa aleta vahingossakaan keräämään toisen node_idn tietoja, vaikka eipä tätä kai pitäisi edes päästä tapahtumaan.
        elif  matkalla == True and cleaned_xy.node_id[val+1] == cleaned_xy.node_id[val]:
            erotellut_reitit[ajokerta].lisaa(ajokerta, cleaned_xy.timestamp[val],cleaned_xy.node_id[val],cleaned_xy["grid_id"][val], cleaned_xy.x_grid[val], cleaned_xy.y_grid[val])
            
        erotellut_reitit[ajokerta].yhdista_tiedot()

=======
        elif row.OUT == True and row.OUT == row.fo_OUT:
            matkalla = False
        
        elif matkalla == True:
            erotellut_reitit[ajokerta].lisaa(ajokerta,row.node_id, row.timestamp,row.grid_id, row.x_grid, row.y_grid, row.dayofweek, row.current_hour, row.speed_kmh, row.distance)
    
>>>>>>> 5aae8586775e71d19e0e5e35aa3c8e8496aeee71
    return erotellut_reitit

def reitit_dataframeksi(reitit):
    """[Luo dataframen, joka sisältää kaikkien kauppareissujen tiedot.]

    Args:
        reitit ([List]): [Sisältää kauppareissu-oliot]

    Returns:
        [DataFrame]: [Palauttaa Dataframen, joka sisältää jokaisen datasta erotellun kauppareissun.]
    """

<<<<<<< HEAD
<<<<<<< HEAD

    kauppareissut = pd.DataFrame(None,None,None,None,None)
    # käysään kaikki reittiobjektit läpi ja muodostetaan lisätään ne vuorollaan dataframeen.
    for kauppareissu in reitit:
        kauppareissu.yhdista_tiedot()
        reitti = pd.DataFrame(kauppareissu.tiedot)
        # Lisätään kaikki ajokerrat vuorollaan dataframeen.
        kauppareissut = kauppareissut.append(reitti,  ignore_index=True)
=======
    kauppareissut = pd.DataFrame(None,None,None,None,None)
    reitt = []
    kauppareissut = kauppareissut.append([pd.DataFrame({"ajokerta":a.ajokerta, "node_id":a.node_id, "timestamp":a.timestamp, "x":a.x, "y":a.y,"grid_id":a.ID, "kesto":a.timestamp[-1]-a.timestamp[0] }) for a in reitit])
>>>>>>> 5aae8586775e71d19e0e5e35aa3c8e8496aeee71
=======
    kauppareissut = pd.concat([pd.DataFrame({"ajokerta":a.ajokerta, "node_id":a.node_id, "timestamp":a.timestamp, "x":a.x, "y":a.y,"grid_id":a.ID, "speed_kmh":a.speed_kmh,"distance":a.distance, "kesto":a.timestamp[-1]-a.timestamp[0], "dayofweek":a.weekday, "current_hour":a.hour}) for a in reitit])
>>>>>>> beea667bbf3b3610ca5a22997bc8b4c63b610fb1
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

def plot_unique_routes(df_reitit, grid_size, in_x, in_y, out_x, out_y):
    """[Plottaa jokaisen kauppareissun peräkkäin]

     Args:
         df_reitit ([DataFrame]): [Sisältää erotellut kauppareitit]
         grid_size ([int]): [Gridin koko on määritelty tämän mukaan.]
     """
    ajot = df_reitit["ajokerta"].unique()
    df_reitit["color"] = np.arange(0,len(df_reitit),1)
    for ajo in ajot:
        print(len(df_reitit[df_reitit["ajokerta"] == ajo]))

        facet = sns.scatterplot(x="x", y="y", data=df_reitit[df_reitit["ajokerta"] == ajo],  hue="color")
        sns.scatterplot(x=in_x, y=in_y)
        sns.scatterplot(x=out_x, y=out_y)
        facet.set_xticks(np.arange(0, grid_size+1,10))
        facet.set_yticks(np.arange(0, grid_size+1,10))
        plt.legend([],[], frameon=False)
        plt.show()
        
<<<<<<< HEAD
=======
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
>>>>>>> 5aae8586775e71d19e0e5e35aa3c8e8496aeee71

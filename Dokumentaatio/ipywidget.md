# Ipywidget alusta(main2) + widgets-moduuli


## Ipywidget alusta 

Vaatii seuraavia kirjastoja ja osia:
```python
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
import ipywidgets as widgets
```
## Widgettien asetukset

Määritellään tuleville widgeteille arvot esim. Nodes-valitsimelle 'ALL' sekä 1-32 numerointi.

Nämä ovat määriteltynä ***moduulit/widgets.py*** tiedostossa

```python
# Tunnit widgettien vaihtoehdoiksi
OptHours = list(range(8, 23))

 # Nodeidt listaan
nodeIds = []
nodeIds.append("All") 
for i in range(32):
    nodeIds.append(i+1)
```


### @interact_manual toiminto
- Laitetaan solun alkuun ja vaatii ```def widgets(widgets_here):``` perään, josta haetaan annetut widgetit
- Lisää "**Run Interact**" napin UI:hin josta saadaan päivitettyä muutokset


Widgets lista löytyy [täältä](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html)

```python
@interact_manual

def dataoptions(
    
    nodes = widgets.SelectMultiple(options= nodeIds,value=['All'],description='Node_id(s): ', disabled=False, layout=Layout(margin='0px 0px 40px 200px')),

    start_date=widgets.DatePicker(value=pd.to_datetime('2020-05-01'),description='Starting Date', layout=Layout(margin='0px 0px 0px 0px')),                      
    end_date=widgets.DatePicker(value=pd.to_datetime('2020-11-01 23:00:00'),description='Ending Date', layout=Layout(margin='-30px 0px 0px 400px')),
                           
    tuntivalitsin=widgets.SelectionRangeSlider(options=OptHours,index=[0,14],
    description='Tunnit',disabled=False,value=[8,22], layout=Layout(margin='20px 0px 0px 0px')),

   ):
```

# getdata() funktio

- Hakee halutun datan suoraan tietokannasta.
- Käyttää **global df** koska en osaa palauttaa dataframea muuten
## 1. Tietokantayhteys ja päivämäärät (start_date/end_date) muuttujat str-muotoon
- **.format** funktiolla saadaan päivämäärät haluttuun muotoon, joka kelpaa sql kyselyyn
``` python
@interact_manual

def dataoptions(...):
    
    def getdata():
        
        global df
        import mysql.connector
        mydb = mysql.connector.connect(
        host="172.28.200.50",
        user="root",
        port=3306,
        passwd="insert-password-here",
        database="iiwari_org")
        
        mycursor = mydb.cursor(dictionary=True)
        
        # Paivmaarat string formaattiin
        start_date_string = "'{}'".format(str(start_date))
        end_date_string = "'{}'".format(str(end_date))
```


## 2. SQL-kyselyt perustuen nodejen valintaan ('All', 1, (1,...,32))

Jos valittuna 'All' valitaan kaikki nodet ja suodatetaan myös valituin *start/end_date* mukaan
- .format(muuttuja1, muuttuja2) laittaa arvot {} {} kohtiin

Lopuksi haetaan saatu dataframe .fetchall() funktiolla, Jos dataframe on tyhjä niin palautetaan virheilmoitus

```python
        # Sql kysely vaihtoehdot jos valittu 'All'
        if nodes[0] == 'All':
            mycursor.execute("SELECT * FROM CleanSensorData WHERE timestamp >= {} and timestamp < {}".format(start_date_string, end_date_string))
            
        # Jos vain 1 node valittu
        elif len(nodes) == 1:
            mycursor.execute("SELECT * FROM CleanSensorData WHERE node_id={} and timestamp >= {} and timestamp < {}".format(nodes[0], start_date_string, end_date_string))
        
        # Monta nodea valittuna
        else:
            mycursor.execute("SELECT * FROM CleanSensorData WHERE node_id IN {} and timestamp >= {} and timestamp < {}".format(nodes, start_date_string, end_date_string))
            
        df = pd.DataFrame(mycursor.fetchall())
        
        # Palauttaa virheilmoituksen jos dataframe on tyhja
        if len(df) == 0:
            return print("Error 01: Empty Dataset ")
```

## 3. Tuntien suodattaminen dataframessa

Tätä ei voinut suorittaa tietokanta kyselyssä joten teemme sen dataframessa. Muunnetaan timestamp str muotoon ja .loc toiminnolla suodatetaan annettujen tuntien mukaan.



```python
        # Timestamp datetime muotoon
        df['timestamp'] = df['timestamp'].astype(str)
        df['timestamp'] = df['timestamp'].str.slice(2, -2)
        df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
        
        # Sorttaa tunnit                   
        df = df.loc[df.timestamp.dt.strftime('%-H').astype('int32') >= tuntivalitsin[0]]
        df = df.loc[df.timestamp.dt.strftime('%-H').astype('int32') <= tuntivalitsin[1]]
        
        return df

```


## 4. Dataframen palautus, getdata() funktion suorittaminen ja lopputulos

Loppuun lisätään getdata()-funktion suorittaminen ja dataframen palautus.
```python
@interact_manual

def dataoptions(...):
    
    def getdata():
        ...
        ...
        return df
    
    # Suoritetaan getdata
    df = getdata()
   
    # Palauttaa dataframen
    return df
```


Kun Run Interactiä painaa niin tietokantahaku lähtee käyntiin ja lopputulos tallentuu automaattisesti **df**-nimiseen dataframeen
![](https://gitlab.dclabra.fi/wiki/uploads/upload_48357bed59e64745538cf44f818a6a41.png)

## Widgets moduuli - Widgettien kutsuminen

Tämä onnistuu yksinkertaisesti kutsumalla display("halutus widgetit") + sort_by_widgtes() funktioilla esim. jos halutaan suodattaa dataframesta tunteja niin:


![](https://gitlab.dclabra.fi/wiki/uploads/upload_7cb31978b2cbb5a7fa1084dfd17402a4.png)

Display()- funktiolla voi kutsua ```start_date, end_date, tunnit``` widgettejä yhden tai useita
sort_by_widgets ottaa sisään dataframen, josta sitten suodatetaan halutut arvot.

[InfluxDB Dockerilla (Linux)](https://hub.docker.com/_/influxdb/)

[InfluxDB Dockerilla (Windows 10)](https://www.open-plant.com/knowledge-base/how-to-install-influxdb-docker-for-windows-10/)

[[_TOC_]]

InfluxDB on Go:lla koodattu aikasarjatietokanta (time series database), joka eroaa relaatiotietokannoista.

Aikasarja on periaatteessa sarja pisteitä, jotka on indeksoitu aikajärjestyksessä. Kaikilla sarakkeilla on siis erityinen aikasarake.

Esimerkkejä aikasarjan tiedoista ovat:
- Työttömyyden tason mittaaminen jokaisen kuukauden aikana
- Enemmän tietyllä hetkellä myydyn tuotteen seuranta verkkokauppasivustolla.
- Seuraavan tuotteen seuranta verkkokaupan verkkosivustolla
- Säännöllisin väliajoin otettujen osakkeiden ja osakkeiden hinta.

## Käyttöliittymä
InfluxDB tarjoaa 2 käyttöympäristöä:
- UI selaimessa
- Terminaali

# Docker

## Kontin pystytys

Linux:

`$ docker run -p 8086:8086 -v $PWD:/var/lib/influxdb influxdb`

CLI/SHELL:
```
docker run --name=influxdb -d -p 8086:8086 influxdb
docker exec -it influxdb influx
```

`PS> docker run -p 8086:8086 -v ${PWD}:\GitHub\Erik\projekti-2-team-fox\Tietokannat\InfluxDB influxdb`

Se miten itse loin Windows 10:llä:

`docker run --name influxdb -p 8086:8086 -v D:\GitHub\Erik\projekti-2-team-fox\Tietokannat\InfluxDB:/var/lib/influxdb influxdb -config /var/lib/influxdb/influxdb.conf`
- Ensin on tuo polku minne tallennan tietokanna omalla koneella
- Erotettu : on influDB:n polku, mikä on sidottu kiinni oman koneeni polkuun.
- -config käynnistää ottamalla config-tiedoston huomioon (joka vaaditaan jos tahtoo käynnistää adminina)

<dl>
  <dt>InfluxDB käyttää portteja</dt>
  <dd>8086 HTTP API portti</dd>
  <dd>2003 Graphite support (jos on päällä)</dd>
</dl>

HTTP API portti avautuu automaattisesti docker run -P kommennon suoritettua.

<d1>
  <dt>Huom:</dt>
  <dd>Oletuksena InfluxDB lähettää telemetriatiedot takaisin InfluxDataan. InfluxData-telemetriasivu tarjoaa tietoja siitä, mitä tietoja kerätään ja miten niitä käytetään.</dd>
  <dd>Jos haluaa estää telemetriatietojen lähettämisen takaisin InfluxDataan, lisätään `--reporting-disabled` komennon loppuun käynnistettäessä InfluxDB-konttia.</dd>

---

# InfluxDB
## InfluxDB:n toiminta

InfluxDB on hieman erilainen muihin tietokantoihin verrattuna:

| InfluxDB | SQL |
| :--- | :---: |
| measurements | taulu |
| tags | indeksoitu kolumni |
| field | indeksoimaton kolumni |

InfluxDB tarvitsee vähintään yhden käyttäjän: Adminin.

Avataan konsoli tietokantaan:

`docker exec -it influxdb /bin/bash`

Luodaan Admin-käyttäjä tietokannassa:

`CREATE USER admin WITH PASSWORD 'teamfox' WITH ALL PRIVILEGES`

Mene sisälle tietokantaan adminina:

`docker exec -it influxdb influx -username admin -password teamfox`

Nyt, kun menee selaimeen ja menee osoitteeseen http://localhost:8086/query?q=show databases, nähdään tietokanta.

### Tietokantaa lisääminen

`CREATE DATABASE <tietokanta>`

`USE <tietokanta>`

`INSERT sensordata,node_id=0i timestamp="empty",x=0i,y=0i,z=0i,q=0i`

| data point | merkitys | 
| :--- | :---: |
| sensordata | measurement |
| node_id | tag set |
| timestamp | field set |
| x | field set |
| y | field set |
| z | field set |
| q | field set |

Merkkijonot on laitettava lainausmerkkeihin vain, kun niitä käytetään _field_-arvoina.

Näytä koko "taulu":

`SELECT * FROM sensordata`

Tee csv tiedosto taulukosta root-kansioon:

`influx -username admin -password teamfox -database iiwari_org -execute "SELECT * FROM sensordata" -format csv > test.csv`

## Populointi

[Tutoriaali csv tiedoston lukemisen Influxiin:](https://medium.com/@dganais/getting-started-writing-data-to-influxdb-54ce99fdeb3e)

Valitettavasti, InfluxDB ei tue suoraan csv.tiedoston lukemista tietokantaa, vaan ne pitää muuttaa tekstitiedostoksi, jossa rivit ovat InfluxDB:n ymmärtäviä line protokollaa.

Tehdään tämä Pythonilla:

### Alustus
Otetaan csv-tiedosto käyttöön:
```python=
import pandas as pd

df = pd.read_csv("./node_3200.csv")
df["measurement"] = ['sensordata' for t in range(len(df))]
df.head()
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_7799c97d3be6d7af01015acab17278b6.png)

Muutetaanpas tuo '*timestamp*' vielä järkevään muotoon:
```python=
df['timestamp'] =df['timestamp'].astype(str)
df['timestamp'] = df['timestamp'].str.slice(2, -7)

df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
df['timestamp'] = pd.Series(df['timestamp']).dt.round("S")
df
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_3dc5744004b76d16500f6230eef61d75.png)

### Formatointi tekstitiedostoon
Ja näin se pitää formatoida tekstitiedostoon (Huom, "q" kolumnia ei otettu mukaan):
```python=
lines = [str(df["measurement"][d]) 
         + ",type=BTC" 
         + " " 
         + "timestamp=" + str(df["timestamp"][d]) + "," 
         + "x=" + str(df["x"][d]) + ","
         + "y=" + str(df["y"][d]) + ","
         + "z=" + str(df["z"][d]) + ","
         + "node_id=" + str(df["node_id"][d]) for d in range(len(df))]
```

Tältä se näyttää:
```
sensordata timestamp="2007-03-19 11:46:19",x=0,y=0,z=0,node_id=3200
sensordata timestamp="2007-03-19 11:46:20",x=0,y=0,z=0,node_id=3200
sensordata timestamp="2007-03-19 11:46:21",x=0,y=0,z=0,node_id=3200
sensordata timestamp="2007-03-19 11:46:22",x=0,y=0,z=0,node_id=3200
```

### Populointi monella tiedostolla

Yhdistetään kaikki csv tiedostot yhdeksi
```python=
import pandas as pd
import glob

path = r'/home/jovyan/work/projekti-2-team-fox/' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)
df
```
![](https://gitlab.dclabra.fi/wiki/uploads/upload_62067342a40efd5525a50ced89f6f556.png)

Lisätään measurement
```python=
df["measurement"] = ['sensordata' for t in range(len(df))]
df.head()
```

Muutetaan tekstitiedostoon
```python=
import random

@timerfunc

def convert():
    
    %time
    
    lines = [str(df["measurement"][d]) 
             + " " 
             + 'timestamp="' + str(df["timestamp"][d]) + '",' 
             + "x=" + str(df["x"][d]) + ","
             + "y=" + str(df["y"][d]) + ","
             + "z=" + str(df["z"][d]) + ","
             + "q=" + str(df["q"][d]) + ","
             + "node_id=" + str(df["node_id"][d]) for d in range(len(df))]
    return lines

def write_to_txt(text):
    thefile = open('import.txt', 'a+')
    for item in text:
        thefile.write("%s\n" % item)
        
if __name__ == '__main__':
    write_to_txt(convert())
```

Kummassakin esimerkissä:

Tämä pitää lisätä tekstitiedoston alkuun:

```
# DDL
CREATE DATABASE iiwari_org
# DML
# CONTEXT-DATABASE: iiwari_org
```

- **DDL** luo autogeenitietokannan nimeltä "*iiwari_org*". 
- **DML** määrittää, mitä tietokantaa käytetään, jos olet jo luonut tietokannan.

### Tietokannan populointi tekstitiedostosta
Tällä loitsulla sitten populoidaan tietokanta:

```influx -import -path=/var/lib/influxdb/import.txt -precision=ns -username admin -password teamfox```

Käsittelyn jälkeen, lopussa tulostuu näin:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_31277d0c07eea9458bb2dca0ce0efe4e.png)

Voidaan tarkistaa miten populointi onnistui:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_b269e41fe07aa86147735b52afd63d19.png)

## Tietokannasta lukeminen Pythonilla

Näin datan voi lukea localhostilla:

```python=
import pandas as pd
from influxdb import InfluxDBClient

# Alustetaan influxing client, täytetään tiedot
client = InfluxDBClient(host='localhost', port=8086, username='admin', password='teamfox')

# Tämä on periaatteessa "SHOW DATABASES" komento influxissa
client.get_list_database()

# "USE iiwari_org"
client.switch_database('iiwari_org')

# Tehdään hakeminen
tables = client.query('SELECT * FROM sensordata LIMIT 20')

# Käydään rivit läpi
test = []
for table in tables:
    # Lisätään listaan
    test.append(table)

# Lisätään pandasin dataframeen
for i in test:
    df = pd.DataFrame.from_dict(i)
df
```
Tulos:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_b5377b7066acc8ed5c700644e0c239c8.png)


---

## (Ei toimi) Tietokannan populoiminen InfluxDB Cloudiin

Tehdään samat alku valmistelut kuin edellisessä kohdassa, mutta ei kirjoiteta dataa tekstitiedostoon vaan suoraan InfluxDB Cloudiin:
```python=
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Täytetään tiedot.
# Tokenin voi luo InfluxDB Cloudin UI:ssa "Data" > "Tokens"
token = "F3TMKn-fKxzeT_XNWMl073TDcDdg-27OaxJtc-FC3NW1vO4Wx-SV3Vrhoju5a5vGvyJC4yEFO5zlqNONExXlqg=="
org = "eriko.oy38@gmail.com"
bucket = "eriko.oy38's Bucket"

# Alustetaan client
client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)

# Alustetaan write-API
write_api = client.write_api(write_options=SYNCHRONOUS)

# Muutetaan datasetti pandasin dataframiksi
dataframe = pd.DataFrame(df)

# Kirjoitetaan tietokantaan
write_api.write(bucket.name, record=dataframe, data_frame_measurement_name='sensordata')

# Suljetaan client
write_api.__del__()
client.__del__()
```

---
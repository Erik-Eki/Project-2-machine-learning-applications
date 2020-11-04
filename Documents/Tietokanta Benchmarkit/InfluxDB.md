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
## InfluxDB dockerilla
Influxillekin on ihan oma image, mutta siihen on vaikeampi asentaa riippuvuuksia enkä saanut sitä toimimaan.

Kuten mainittu edellisessä osiossa, ***Influxdb ei tue suoraan csv-tiedostosta kirjoittamista***, csv tiedosto pitää ensin muuttaa influxin line-protokollaan.

Tietokannan populointiin käytän [**Fabio Mirandan csv-to-influx python scriptiä**](https://https://github.com/influxdata/influxdb-comparisons).
Jos tietokanta populoitaisiin reaaliajassa, ei bulkkina, ei pythonia tarvitsisi tässä tilanteessa.

Vaatimukset:
- Python3
- pip3
    - Asennetaan python-paketit: ```requests, argparse, python-csv, datetime, pytz, influxdb```
- Influxdb
    - Vaatii ```gnupg2, curl```
- nano (Tai mikä vain tekstieditori. Ihan vain jos haluaa kikkailla kontissa)

## Dockerfilen luonti

**FROM** hakee pohja imagen
```dockerfile=
# Set base image (host OS)
FROM ubuntu:latest
```

Luodaan "työpöytä" **WORKDIR** komennolla
```dockerfile=
# Set the working directory in the container
WORKDIR ./
```
Avataan portti 8086 **EXPOSE** komennolla
```
# Expose port 8086
EXPOSE 8086
```

Muutetaan default shell bashiksi **SHELL** komennolla
(Tämä siksi, koska jotkin komennot, kuten "source" ei toimi muuten)
```
# Establish default shell
SHELL ["/bin/bash", "-c"] 
```
**RUN** komento on sama asia kuin ajaisi normaalin komennon terminaalissa

RUN komennon **default shell** on **"/bin/sh"**, siksi se piti vaihtaa edellisessä kohdassa.

**-y** tarkoittaa "assume yes", eli aina kun terminaalissa pitäisi painaa yes/no, painaa se automaattisesti "yes"
```dockerfile=
# Installing the main dependancies
RUN apt-get update -y && apt-get upgrade -y

RUN apt install nano -y && \
	apt install -y gnupg2 curl -y && \
	apt install python3 -y && \
	apt install python3-pip -y
```

**COPY** komento kopioi kansion tai tiedoston local-koneelta konttiin
```dockerfile=
# Copy the content of the local src directory to the working directory
# The database population python-script is in here.
COPY csv-to-influx/ .
```

Näin voi asentaa **dependencyjä**, esim tässä tilanteessa *python paketteja*
```dockerfile=
# Copy the dependencies list to the working directory
COPY requirements.txt .

# Install dependencies used by the population python-script
RUN pip3 install -r requirements.txt
```
requirements.txt näyttä yksinkertaiselta:
```
requests
argparse
python-csv
datetime
pytz
influxdb
```

Asennetaan influxdb
```dockerfile=
# Setting up influxdb
# Import GPG key
RUN curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
RUN source /etc/lsb-release
# Add repo for Ubuntu 20.04
RUN echo "deb https://repos.influxdata.com/ubuntu bionic stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt update -y
RUN apt install -y influxdb
```
Influxin repon komento meinaa siis: ```RUN echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable"```

Influxilla on configurointi tiedosto, johon pitää tehdä muutoksia.
```dockerfile=
# Replace default influx.conf with custom one
RUN rm /etc/influxdb/influxdb.conf
COPY influx-conf/ /etc/influxdb
```
Muutokset:
```python=
[http]
# Determines whether HTTP endpoint is enabled.
  enabled = true
# Determines whether the Flux query endpoint is enabled.
  flux-enabled = true
# Determines whether the Flux query logging is enabled.
# The bind address used by the HTTP service.
  bind-address = ":8088"
# Determines whether user authentication is enabled over HTTP/HTTPS.
  auth-enabled = true
```

Influxdb pitää käynnistää
```dockerfile=
# Start influx service
RUN service influxdb start
```

Luodaan admin käyttäjä influxiin
```dockerfile=
# Creating an admin user for influx
RUN curl -XPOST "http://localhost:8086/query" --data-urlencode "q=CREATE USER admin WITH PASSWORD 'teamfox' WITH ALL PRIVILEGES"
# Testing if the influx works
RUN curl -G http://localhost:8086/query -u admin:teamfox --data-urlencode "q=SHOW USERS"
```

Kopioidaan tietokantaa puskettava data locaalista kansiosta
```dockerfile=
# Copy the sensordata into the container
#COPY data .
```

Kopioidaan populointi scripti
```dockerfile=
# Copy the database population script into container
COPY populate-script/ .

# Making the txt.file an executable with chmod and running it
RUN chmod +x populate.sh
```
Populointi scripti käy data kansion läpi, jossa on .csv tiedostot.
```bash=
for file in ./data/*; do
	python3 csv-to-influxdb.py --user admin --password teamfox --dbname iiwari_org -m SensorData -tf "%Y-%m-%d %H:%M:%S.%f+00:00" --input "$file" --tagcolumns node_id --fieldcolumns x,y,z,q -b 200000
done
```

**CMD** komentoa ei suoriteta build-vaiheessa vaan ***kontin luomisen jälkeen*** ja vain yksi CMD-komento sallitaan (jos on enemmän, vain viimeinen ajetaan)
```dockerfile=
# Run the population script
CMD ["bash", "populate.sh"]
```

## Kontin pystytys
Linux:

`$ docker run -t -d --name influxDB -p 8086:8086 influxdb`

CLI/SHELL:
```
docker run --name=influxdb -d -p 8086:8086 influxdb
docker exec -it influxdb influx
```

`PS> docker run -p 8086:8086 -v ${PWD}:\GitHub\Erik\projekti-2-team-fox\Tietokannat\InfluxDB influxdb`

Esimerkki:
`docker run --name influxdb -p 8086:8086 -v D:\GitHub\Erik\projekti-2-team-fox\Tietokannat\InfluxDB:/var/lib/influxdb influxdb -config /var/lib/influxdb/influxdb.conf`
- Ensin mountataan **-v** tuo polku minne tallennan tietokanna omalla koneella
- **:** on erotettu influDB:n polku, mikä on sidottu kiinni oman koneeni polkuun.
- **-config** käynnistää ottamalla config-tiedoston huomioon (joka vaaditaan jos tahtoo käynnistää adminina)

<dl>
  <dt>InfluxDB käyttää portteja</dt>
  <dd>8086 HTTP API portti</dd>
  <dd>8088 Influxin Backup ja Restore</dd>
</dl>

HTTP API portti avautuu automaattisesti docker run -P kommennon suoritettua.

<d1>
  <dt>Huom:</dt>
  <dd>Oletuksena InfluxDB lähettää telemetriatiedot takaisin InfluxDataan. InfluxData-telemetriasivu tarjoaa tietoja siitä, mitä tietoja kerätään ja miten niitä käytetään.</dd>
  <dd>Jos haluaa estää telemetriatietojen lähettämisen takaisin InfluxDataan, lisätään `--reporting-disabled` komennon loppuun käynnistettäessä InfluxDB-konttia.</dd>

---

# InfluxDB perusteet
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

## Tietokantaa lisääminen

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

# Python

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

## Formatointi tekstitiedostoon
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

## Populointi monella tiedostolla

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

## Populointi tekstitiedostosta
Tällä loitsulla sitten populoidaan tietokanta:

```influx -import -path=/var/lib/influxdb/import.txt -precision=ns -username admin -password teamfox```

Käsittelyn jälkeen, lopussa tulostuu näin:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_31277d0c07eea9458bb2dca0ce0efe4e.png)

Voidaan tarkistaa miten populointi onnistui:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_b269e41fe07aa86147735b52afd63d19.png)


## Lukeminen pythonilla

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
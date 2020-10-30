### Timescaledb

TimescaleDB on avoimen lähdekoodin tietokanta ja sen hallintajärjestelmänä toimii PostgreSQL. TimescalesDB on optimoitu toimimaan nopeasti aikasarjallisen datan kanssa. 
TimescaleDB on vakaa tietokanta, ja se toimii parhaiten järjestelmissä, jossa dataa tulee todella paljon monista eri lähteistä.


Dockerilla tietokanta saadaan pystyyn ajamalla alla oleva bash-skripti. Skripiti tulee ajaa kansiossa, jossa tietokantaan siirrettävä data sijaitsee, tai vaihtoehtoisesti ${PWD} tulee korvata polulla datan sisältävään kansioon.

Luodaan siis tiedosto populate_timescaledb.sc samaan kansioon datan kanssa:

`touch populate_timescaledb.cs`

`sudo nano populate_timescaledb`

 Ja kopioidaan alla oleva scripti siihen.

```
#!/usr/bin/env  bash

# Luo TimescaleDB kontin. Lataa imagen, jos sitä ei valmiiksi ole koneella.
docker run -d -t -i --name timescaledb_fox -p 5432:5432 -e POSTGRES_PASSWORD=password  timescale/timescaledb:1.7.4-pg12
sleep .5s

# Kopioi kansion kontin sisälle.
docker cp ${PWD} timescaledb_fox:/home/
sleep .5s

# Tarkistaa onko database jo olemassa (ei oikeastaan edes tarvita, mutta teinpähän huvikseni)
docker exec -i timescaledb_fox psql -U postgres -c "DROP DATABASE IF EXISTS iiwari;"

# Luodaan database
docker exec -i timescaledb_fox psql -U postgres -c "CREATE DATABASE iiwari;"
sleep .5s

# Kirjaudutaan databaseen ja tehdään siitä Timescaledb (Oletuksena luodaan PostgreSQL)
docker exec -i timescaledb_fox psql -U postgres -d iiwari -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

# Tätäkään ei tarvita, mutta tarkistetaan onko taulu jo olemassa, ja jos on niin poistetaan.
docker exec -i timescaledb_fox psql -U postgres -d iiwari -c "DROP TABLE  IF EXISTS sensordata;"

# Luodaan taulu. Node_id:n tietotyyppinä kannattaisi olla integer, mutta se on nyt float, koska myöhemmin käytettävässä datassa integer ei kelpaa.
docker exec -i timescaledb_fox psql -U postgres -d asdasd -c "CREATE TABLE sensordata ( node_id FLOAT NOT NULL,  
timestamp TIMESTAMPTZ,  x INT NOT NULL,  y INT NOT NULL,  z INT NOT NULL,  q INT NOT NULL);"
sleep .5s

# Tehdään taulusta hypertable (hypertable jakaa taulun pienempiin osiin timestampin perusteella)
docker exec -i timescaledb_fox psql -U postgres -d iiwari -c "SELECT create_hypertable('sensordata', 'timestamp');"

sleep .5s
# Kopioidaan data tietokantaan
docker exec -i timescaledb_fox psql -U postgres -d iiwari -c "COPY sensordata FROM PROGRAM 'awk FNR-1 /home/data/*.csv | cat'  CSV HEADER;"
sleep .5s

# Poistetaan datan sisältävä kansio kontin sisältä
docker exec -i timescaledb_fox bash -c "rm -rf /home/data"
```
Jotta skripti voidaan ajaa, täytyy sen oikeuksia muuttaa terminaalissa:
`sudo chmod 755 populate_timescaledb.sc`

Nyt scripti voidaan suorittaa:
`./populate_timescaledb.sc`

![](https://gitlab.dclabra.fi/wiki/uploads/upload_a775a8e6c7e89fa25ce7f7bb029a8a0f.png)

Nyt kaikki data on tietokannassa.

Tarvittaessa tietokanta saadaan poistettua ajamalla terminaalissa:

`docker stop timescaledb_fox && docker rm timescaledb_fox`

### Yhteyden ottaminen tietokantaan localhostissa

Aluksi etsitään ip-osoite, jota tietokantakontti käyttää:
`docker inspect timescaledb_fox`

Osoite löytyy tulosteen lopusta:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_9da7ae7a533ce681c79e1139454a8191.png)

Luo uusi python-tiedosto haluamallasi editorilla.

Pythonilla tietokantaan saadaan yhteys psycopg2-kirjastolla, joten ladataan se terminaalissa.
`pip3 install psycopg2-binary`

Seuraavalla koodilla saadaan yhteys tietokantaan, sekä luotua haetusta datasta dataframe.

```=python
import psycopg2
import pandas as pd
import time

# Luodaan yhteys
connection = psycopg2.connect(user = "postgres",
                              password = "password",
                              host = "172.17.0.1",
                              port = "5432",
                              dbname = "iiwari")
cursor = connection.cursor()
# Tehdään kysely tietokantaan, ja kellotetaan kauan se kestää.
start = time.time()
cursor.execute("SELECT * from sensordata limit 10000000;")
print("Query time:", time.time()- start)

# Luodaan haetusta datasta dataframe.
column_names = ["node_id", "timestamp", "x", "y", "z", "q"]
df = pd.DataFrame(cursor.fetchall(), columns=column_names)

# Suljetaan yhteys
if(connection):
    cursor.close()
    
df.head(10)
```

![](https://gitlab.dclabra.fi/wiki/uploads/upload_40169c2d1232fbf100d6aa7d17e364bd.png)

### Benchmark




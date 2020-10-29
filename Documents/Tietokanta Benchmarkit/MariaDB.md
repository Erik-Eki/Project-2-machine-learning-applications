# Docker

## Kontin pystytys

Aloitetaan käynnistämällä docker kontti jossa pyörii ```mariadb```
```
docker run --name iiwari-mariadb-server -e MYSQL_ROOT_PASSWORD=insert-password-here mariadb:latest
```

### Jos kyseinen kontti on jo luotuna mutta ei päällä virheilmoituksella
- *The container name "/iiwari-mariadb-server" is already in use by container*

Käynnistä kontti komennolla ```docker start kontin-nimi```
Docker konttien nimet saat komennolla ```docker ps```

Kontin sisään pääset kirjatumaan komennolla:
```docker exec -it iiwari-mariadb-server bash```

jonka jälkeen MYSQL serverin sisään:
```mysql -u root -p```

### Seuraavaksi luodaan kyseiset tiedostot:
kopio koodi tekstitiedostoon ja nimeä ne.

**1. Databasen luonti `createdb.sh`**

``` mysql
#!/bin/bash
#cd /var/lib/mysql/iiwari_org
docker exec -i iiwari-mariadb-server /usr/bin/mysql -u root --password=insert-password-here < initdb.sql
```
**2. Tietokannan rakenne `initdb.sql`**
```
CREATE DATABASE IF NOT EXISTS iiwari_org DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin;

USE iiwari_org;

DROP TABLE IF EXISTS SensorData;
CREATE TABLE SensorData (
  node_id INTEGER NOT NULL,
  timestamp TEXT,
  x INTEGER NOT NULL,
  y INTEGER NOT NULL,
  z INTEGER NOT NULL,
  q INTEGER NOT NULL
);
```

**3. Tietokannan populointi `populate-mariadb.sh`**
```
#!/bin/bash
#cd /var/lib/mysql/iiwari_org
for f in ${PWD}/*.csv
do
   echo Working on $f
   docker cp $f iiwari-mariadb-server:/var/lib/mysql/SensorData.csv
   docker exec -i iiwari-mariadb-server /usr/bin/mysqlimport --ignore-lines='1' --fields-terminated-by=',' --user=root --password=insert-password-here iiwari_org "/var/lib/mysql/SensorData.csv"
done
```

Avaa terminaali kansiossa jossa sijaitsee .csv- ja ylläolevat tiedostot ja suorita seuraavat kolme komentoa:
```
chmod 755 ./populate-mariadb.sh ./createdb.sh
./createdb.sh
./populate-mariadb.sh
```

# Mariadb Tietokannan Benchmarkkaus
Käytetyn raudan tiedot:



| OS          |   CPU       | System Memory |Storage | 
| --------    | --------    | --------      |-------|
|Lubuntu 64bit|A6-9225 2C+3G| 7486MiB       |Micron_1100_MTFD ATA Disk 256GB|



Tietokantaan on populoitu 'Node_3200' ja rivejä yhteensä: 129,785,88

Aloitetaan kirjautumalla dockerkontin sisälle:
```
docker exec -it iiwari-mariadb-server bash
```

Jonka jälkeen mysql kirjautuminen:
```
mysql -u root -p
```

### Databasen komentoja:
Näytä kaikki tietokannat = ```SHOW Databases;```  
Tietokannan valinta =  ```USE insert-database-name-here```  
Näytä kaikki Taulut = ```SHOW Tables;```  
Disable STD-output = ```pager cat > /dev/null```  
Enable STD-output = ```pager```
### SQL-kyselyt:
Hae 5 ensimmäistä = ```SELECT * FROM SensorData LIMIT 5```


## Luku-nopeudet:

### OMA RAUTA
Suoritin 10 kertaa koko databasen haun: ```SELECT * FROM SensorData;```

Tuloksiksi sain sekuntteina:
20.071, 19.922, 19.914, 19.786, 19.907,
19.877, 19.845, 19.811, 19.786, 19.937

### BULL BLADE

Tuloksiksi sain sekuntteina:
11.718, 11.724, 11.746, 11.715, 11.696, 
11.687, 11.692, 11.666, 11.710, 11.725

## Kirjoitus-nopeudet

### OMA RAUTA

10 kertaa suoritettu ```time ./populate-mariadb.sh```

Tulokset sekuntteina:
37.147, 34.714, 35.078, 34.781, 34.957,
34.957, 35.015, 35.270, 35.882, 36.610

### BULL BLADE

Tulokset sekuntteina:
80.089, 81.282, 79.223, 78.801, 78.504,
78.629, 78.659, 77.972, 80.684, 79.761
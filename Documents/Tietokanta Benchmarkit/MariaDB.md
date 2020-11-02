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

# Mariadb Tietokannan Benchmarkkaus Bullilla


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

`SELECT * FROM SensorData WHERE Node_id=3200;`

Tuloksiksi sain sekuntteina:
151, 144, 122, 128, 118,  
135, 124, 119, 122, 117

## Kirjoitus-nopeudet

**Populoitu siis node_3200.csv tietokantaan**

Tulokset sekuntteina:
80.089, 81.282, 79.223, 78.801, 78.504,
78.629, 78.659, 77.972, 80.684, 79.761
[InfluxDB Dockerilla (Linux)](https://hub.docker.com/_/influxdb/)

[InfluxDB Dockerilla (Windows 10)](https://www.open-plant.com/knowledge-base/how-to-install-influxdb-docker-for-windows-10/)

[[_TOC_]]

# InfluxDB
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

Näytä koko "taulu":

`SELECT * FROM sensordata`

Tee csv tiedosto taulukosta root kansioon:

`influx -username admin -password teamfox -database iiwari_org -execute "SELECT * FROM sensordata" -format csv > test.csv`
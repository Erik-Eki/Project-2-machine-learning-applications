[InfluxDB Dockerilla (Linux)](https://hub.docker.com/_/influxdb/)

[InfluxDB Dockerilla (Windows 10)](https://www.open-plant.com/knowledge-base/how-to-install-influxdb-docker-for-windows-10/)

[[_TOC_]]

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

## InfluxDB

InfluxDB on hieman erilainen muihin tietokantoihin verrattuna:
| :--- | :---: |
| measurements | SQL taulu |
| tags | indeksoitu kolumni |
| field | indeksoimaton kolumni |

`docker exec -it influxdb /bin/bash`

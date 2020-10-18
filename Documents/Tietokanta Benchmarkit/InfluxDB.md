[InfluxDB Dockerilla (Linux)](https://hub.docker.com/_/influxdb/)

[InfluxDB Dockerilla (Windows 10)](https://www.open-plant.com/knowledge-base/how-to-install-influxdb-docker-for-windows-10/)

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

InfluxDB käyttää portteja
: 8086 HTTP API portti
: 2003 Graphite support (jos on päällä)

HTTP API portti avautuu automaattisesti docker run -P kommennon suoritettua.

Huom:
: Oletuksena InfluxDB lähettää telemetriatiedot takaisin InfluxDataan. InfluxData-telemetriasivu tarjoaa tietoja siitä, mitä tietoja kerätään ja miten niitä käytetään.
: Jos haluaa estää telemetriatietojen lähettämisen takaisin InfluxDataan, lisätään `--reporting-disabled` komennon loppuun käynnistettäessä InfluxDB-konttia.

## InfluxDB komentorivi

`docker exec -it influxdb /bin/bash`

### YugabyteDB tietokannan luonti

#### Yhteys bulliin

    Osoite: ryhma3@ai.dclabra.fi portti: 30050 alasana: KolmosRyhmä
    SSH-yhteys: ssh ryhma3@ai.dclabra.fi -p 30050
    Tiedostojen lataaminen sshpass ja scp:llä:
    scp -r -P 30050 ryhma3@ai.dclabra.fi:data/node_3200.csv /local/path/

Ladataan tiedostot serveriltä koneelle.

#### Luodaan oma verkko dockeriin missä voidaan käyttää jupyteria

    docker network create mun-oma-verkko --attachable
    docker volume create mun-oma-data # aja vain kerran

###### käynnistä jupyter notebook omalla koneella http://localhost:8888

    docker run --name oma-jupyterlab -e JUPYTER_TOKEN=yes -e GRANT_SUDO=yes -e JUPYTER_ENABLE_LAB=yes --network mun-oma-verkko -v mun-oma-data:/home/jovyan/work -p 8888:8888 jupyter/scipy-notebook:17aba6048f44

#### Tietokannan luonti

Asennetaan yugabyte kirjoittamalla komento: 
    docker pull yugabytedb/yugabyte
Seuraavaksi tehdään paikallinen klusteri komennolla: 
    docker run -d --name yugabytedb-fox  -p7000:7000 -p9000:9000 -p5433:5433 -p9042:9042\ --network mun-oma-verkko\
    -v ~/yb_data:/home/yugabyte/var\
    yugabytedb/yugabyte:latest bin/yugabyted start\
    --daemon=false 

Seuraavaksi tehdään populate-yugabytedb.sh, initdbyugabyte.sql sekä createyugabyte.sh tiedostot joiden sisään laitetaan seuraavat komennot.


###### populate-yugabytedb.sh
    #!/usr/bin/env bash
    #cd /var/lib/mysql/iiwari_org
    for f in ${PWD}/*.csv
    do
        echo Working on $f
        sudo docker cp $f yugabytedb-fox:/var/SensorData.csv
        docker exec -it yugabytedb-fox /home/yugabyte/bin/ysqlsh --echo-queries -d iiwari_org -c "\COPY SensorData FROM '/var/SensorData.csv' WITH     (FORMAT, CSV, HEADER)"
        docker exec -i yugabytedb-fox rm/var/SensorData.csv
    done

###### initdb-yugabyte
    CREATE DATABASE iiwari_org:
    \c iiwari_org
    CREATE TABLE SensorData (
        node_id float NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        z INTEGER NOT NULL,
        q INTEGER NOT NULL);


###### createyugabyte

    #!/usr/bin/env bash
    #cd /var/lib/mysql/iiwari_org 
    docker exec -i yugabytedb-fox /home/yugabyte/bin/ysqlsh         --echo-queries < initdbyugabyte.sql

###### Databasen käynnistys

Kun edelliset tiedostot on luotu voidaan database käynnistää komennolla
    docker run -d --name yugabytedb-fox  -p7000:7000 -p9000:9000 -p5433:5433 -p9042:9042\
    --network mun-oma-verkko\
    -v ~/yb_data:/home/yugabyte/var\
    yugabytedb/yugabyte:latest bin/yugabyted start\
     --daemon=false

Tämän jälkeen kirjoitetaan 
    chmod 755 ./createyugabytedb ./populate-yugabytedb
    ./createyugabytedb
    ./populate-yugabytedb
 
 Populoinnin pitäisi olla nytten käynnissä.




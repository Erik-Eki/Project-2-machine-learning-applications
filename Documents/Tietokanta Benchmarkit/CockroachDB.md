## Cockroachin asennus

- Aloitin itse asentamalla CockroachDB:n dockerille, se tapahtui seuraavalla loitsulla:

`sudo docker pull cockroachdb/cockroach:v20.1.8`

- seuraavana luotiin bridge network cnotainerille:

`docker network create -d bridge roachnet`

- sitten startataan clusteri:

`docker run -d --name=roach1 --hostname=roach1 --net=roachnet -p 26257:26257 -p 8080:8080  -v "${PWD}/cockroach-data/roach1:/cockroach/cockroach-data"  cockroachdb/cockroach:v20.1.8 start --insecure --join=roach1,roach2,roach3`

- jonka jälkeen alustetaan kontti:

`docker exec -it roach1 ./cockroach init --insecure`

- Seuraavana kontin populointi. Tässä meni paljon aikaa ja lopulta Allun avun saattamana se vihdoin onnistui.
- Aluksi pitää varmistaa, että cockroachin cockroach-data kansiossa on kansio extern. Jos sitä ei ole, se pitää luoda sinne
- Seuraavaksi tulevalla koodirimpsulla voi kirjoittaa koneella olevasta .csv tiedostosta taulun CockroachDB:hen:

```
for f in ${PWD}/*.csv
do
   
    docker cp $f roach1:./cockroach/cockroach-data/extern/ServerData.csv
    docker exec -i roach1 ./cockroach sql --insecure -e "CREATE DATABASE IF NOT EXISTS iiwari; USE iiwari; CREATE TABLE node (
    node_id FLOAT NOT NULL,
    timestamp        TIMESTAMPTZ         NOT NULL,
    x int    NOT NULL,
    y int    NOT NULL,
    z int    NOT NULL,
    q int    NOT NULL
); IMPORT INTO node (node_id, timestamp, x,y,z,q) CSV DATA ('nodelocal://self/ServerData.csv') WITH SKIP = '1'"
    docker exec -i roach1 rm -rf cockroach/cockroach-data/extern/ServerData.csv
done
```
- Koodissa kohdat: Alussa looppi lukee kaikki sen hetkisessä sijainnissa olevat .csv tiedostot, jonka jälkeen tekee seuraavaa:
- Kopioi roach1 externiin csv- tiedoston
- Luo iiwari databasen, johon taulun missä yllä olevat attribuutit'

- Benchmarkkaukseen en vielä kerennyt ja siihen perehdyn tulevina päivinä.

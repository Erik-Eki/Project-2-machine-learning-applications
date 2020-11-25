### Puuttuvien päivien etsiminen datasetistä

- Aluksi otimme koko datasetin käsittelyyn, että voimme etsiä kaikki puuttuvat päivät datasta
- Kun datasetin sorttaa timestampin mukaan, huomataan että data on jakautunut aikavälille 5.5.2020 - 23.10.2020.
- Lasketaan pandasin date_rangella monta päivää näiden päivämäärien välistä löytyy:
![](https://gitlab.dclabra.fi/wiki/uploads/upload_2b52aad256294361ee4c4da3fd77cdc0.png)

- Kuten näkyy, päiviä on yhteensä 172.
- Seuraavaksi etsimme dataframesta, kuinka monelta päivältä löydämme data entryjä
- Sen suoritamme seuraavalla tavalla: 
- Aluksi normalisoidaan dataframen timestamp kolumni, jotta sen sisältä päivämäärissä ei löydy tuntejen kohdalta kuin 00.00, näin voimme tarkastella helpommim uniikkeja päivämääriä:
![](https://gitlab.dclabra.fi/wiki/uploads/upload_5f70864bb9cbbec53769d8250ce89c44.png)

- Seuraavaksi voimmekin laskea, monelta eri päivältä timestamppeja löytyy datasetissä:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_4b9c3d53b451b301d03d3ddd23cb9c8f.png)

- Päiviä löytyi 149. Joten nyt voimme laskea, että kaikista päivistä 172, löytyy datasetistä 149, eli päiviä puuttuu 23.
- Viimeisenä reindexoidaan kaikki päivät alkuperäisten päivien joukkoon, että näemme, missä kohdassa kyseistä aikaväliä puuttuvat päivät ovat:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_60acee10743d77fe5bc081b6d2602957.png)

- Puuttuvan päivän kohdalla on nyt NaN eli ei arvoja. Lopuksi plottaamme aikaleimojen määrän per päivä koko aikavälillä nähdäksemme vielä visualisoituna kaikkien päivien timestamppejen määrän ja puuttuvat päivät seassa:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_f2c745d63eaca32bde7b96bb63a34e55.png)

- Tyhjissä aukoissa siis puuttuvat päivät.

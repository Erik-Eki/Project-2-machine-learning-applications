Benchmark -Team Fox
=============
__Tekijät:__ 
Valtteri Alastalo, Kosti Kaaresvirta, Erik Huuskonen, Lauri Pellinen ja Juha Vartiainen.

Testattavat tietokannat ovat YugabyteDB, CockhroachDB, TimescaleDB, MariaDB ja InfluxDB.
Ohjeet jokaisen tietokannan pystyttämiseen ja populoimiseen löytyy [täältä.](https://gitlab.dclabra.fi/ryhm-fox/projekti-2-team-fox/-/tree/master/Documents/Tietokanta%20Benchmarkit)
Testin koodit löytyvät [täältä](https://gitlab.dclabra.fi/ryhm-fox/projekti-2-team-fox/-/tree/Juha/Benchmark).

#### Hakunopeus
Ensimmäisellä testillä mitataan, kuinka nopeasti tietokannasta saadaan haettua 1,400,000 riviä dataa yksinkertaisella kyselyllä, sekä kuinka nopeasti tästä datasta saadaan muodostettua Pandas dataframe. 
![](https://gitlab.dclabra.fi/wiki/uploads/upload_aed83574fa9d96fb8a8f652c714ae283.png)
MariaDB:llä saadaan selvästi nopeiten haettua data, sekä muodostettua dataframe.
Yugabyte:n ja InfluxDB: kyselyt kestivät huomattavasti kauemmin muihin verrattuna. InfluxDB:llä haetusta datasta saadaan kuitenkin muodostettua dataframe lähes yhtä nopeasti, kuin MariaDB:llä.

Toinen testi mittaa hakunopeutta hieman monimutkaisemmalla kyselyllä.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_120b244b06248e5af1657dc91c11916b.png)
MariaDB suoriutuu tässäkin kyselyssä muita nopeammin.
Yugabyte on selvästi muita hitaampi. 
InfluxDB tekee kyselyn nopeammin, kun siihen on asetettu joitan ehtoja verrattuna kyselyyn ilman ehtoja, mutta on silti toiseksi hitain.

#### Kirjoitusnopeus
Kolmas testi mittaa tietokannan kirjoitusnopeutta.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_5c9b5d3df8b4c0a98b3e930d4db93311.png)
CochroachDB:llä tietokantaan saadaan siirrettyä dataa selvästi muita nopeammin(26s).
TimescaleDB:llä aikaa kuluu noin tuplasti Cockhroachiin verrattuna (58s).

#### Skaalautuvuus
Neljännessä testissä mitataan, kuinka kyselyyn kulunut aika kasvaa suhteessa haettavan datan määrään. Tietokantaan tehdään kahdeksan kyselyä. Joka kierroksella kyselyä kasvatetaan 1,000,000 rivillä.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_3befe300dccfb01beb02df4c25076a92.png)
*x-akseli alkaa virheellisesti nollasta.*

Kyselyyn kulunut aika kasvaa lineaarisesti jokaisella tietokannalla, kun haettua rivimäärää kasvatetaan. TimescaleDB:llä ja CochroachDB:llä hakuajoissa on kuitenkin hieman vaihtelua.

InfluxDB:llä tätä testiä ei voitu tehdä, sillä se tallentaa haetun datan muistiin, jonka seurauksena testissä käytetty kone kaatuu testin aikana. Testissä olisi ehkä voitu hakea pienempää määrää dataa, mutta tulemme kuitenkin tekemään vielä suurempia kyselyjä tietokantaan projektin aikana, jonka takia tietokannasta täytyy nämä määrät pystyä hakemaan.

#### Top 3

Yugabyte suoriutui selvästi muita hitaammin kaikissa testeissä, joten se päätettiin tässä vaiheessa tiputtaa pois. Myös InfluxDB tiputettiin, koska se aiheutti ongelmia muistin kanssa.
 
Seuraavissa kuvaajissa voidaan tarkastella lähemmin kolmen nopeimman tietokannan tuloksia.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_7956b2e54c4923cf39aabede24bece6c.png)


Suoritetaan vielä kaksi testiä, joissa data haetaan timestamp:n ja node_id:n perusteella, koska näitä kyselyjä oletettavasti tulemme eniten tietokantaan tekemään.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_fa6ebcd8ea06963ec1aa1ace6c70bb62.png)

*Testissä muodostetaan myös dataframet*

Yllättäen TimescaleDB on näissä testeissä kaikkein nopein.

#### Loppupäätelmät

* CochroachDB:n vahvuutena on kirjoitusnopeus.  Hakunopeus sillä on kuitenkin näistä kolmesta hitain.
* MariaDB:n kirjoitusnopeus on puolestaan selvästi hitain, mutta data saadaan sillä haettua käsiteltäväksi selvästi muita nopeammin, kun kyselyssä ei ole mitään ehtoja.
* TimescaleDB on selvästi nopein, kun kysely sisältää ehtoja. TimescaleDB:llä datan tallentaminen tietokantaan tapahtuu myös toiseksi nopeiten.

-----------
Kaikki benchmarkit ovat suoritettu samalla koneella. 
Tekniset tiedot:

__Suoritin:	Intel®     Core™ i7-10710U 1,1 GHz kuusiydinsuoritin
Keskusmuisti:         16 Gt DDR4 
Kovalevy:	512 Gt NVMe PCIe SSD__





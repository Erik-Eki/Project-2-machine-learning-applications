## Läpimenoaikojen plottauksen dokumentointi

Ensin tarvitaan reittien_erottelu moduulista get_lapimeno funktiota jonka avulla saadaan läpimenojen ajat sekä aloitusajat. Nämä kaksi pitää sitten laittaa plot_lapimeno funktioon.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_1b40c57d99606dbb896403fb28859e2f.png)

Nytten plot_lapimeno laittaa nämä arvot uuteen dataframeen ja näitten perusteella se tekee uudet kellonaika-binit ja laskee sitten keskiarvon kullekkin kellonajalle. Sen jälkeen se plottaa kyseiset keskiarvot.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_a4206c1414dd1157f00164098c2079a3.png)


![](https://gitlab.dclabra.fi/wiki/uploads/upload_dc1ee124d24bd37fac160ab5b2977d4e.png)

Tästä plottauksesta näemme että kello 17-19 kaupassa vietetään eniten aikaa johtuen mahdollisesti siitä että ihmiset pääsevät näihin aikoihin töistä ja käyvät töitten jälkeen varmaankin kaupassa.

Seuraavaksi otetaan dataframen aloituksista viikonpäivät talteen ja laitetaan ne oikeaan järjestykseen(ma-su).
![](https://gitlab.dclabra.fi/wiki/uploads/upload_25dea3a22d3c50053b774ddf6e3e73ad.png)

Tämän jälkeen otetaan keskiarvot joka päivän läpimenoajoista.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_a849eb79c1c12059744364c9861228b5.png)

Ja sitten saaduista tuloksista voidaan plotata joka viikonpäivälle läpimenoaikojen keskiarvo ja näin nähdään mitkä päivät ovat kiireisimpiä.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_46561e12157db9f47bf7764ea3c64deb.png)

Otetulla datamäärällä näyttäisi että perjantai olisi kaikista kiireellisin päivä mikä on arvattavissa sillä ihmiset varmaankin käyvät ostamassa perjantaisin töiden jälkeen viikonlopun ruuat ja juomat. Lauantai taas on viikon hiljaisin päivä mikä ei yllätä sekään.
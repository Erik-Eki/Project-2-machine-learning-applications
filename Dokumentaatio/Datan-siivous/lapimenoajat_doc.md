#### Läpimenoajat dokumentointi

Ensin ohjelmoidaan luokka jossa on kärrit/korit ja timestamppien avulla saadaan tehtyä niistä lista. Tässä listassa on korien/kärryjen node_id:t, timestampit sekä koordinaatit. Näitten avulla voidaan katsoa muutokset kyseisissä muuttujissa ja näiden avulla määritellä ajokerrat.
![](https://gitlab.dclabra.fi/wiki/uploads/upload_1d902689ff027ec7f6a88196574cf0e5.png)


Tämän jälkeen otetaan timestamppien perusteella joka ajokerran läpimenoaika.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_5583088368f5a725949983ea2eef5b0c.png)


Tallennetaan kyseiset läpimenoajat sekä aloitus ajat listaan mikä 
sitten tallennetaan dataframeen. Tähän kannattaa tehdä uusi dataframe. 

![](https://gitlab.dclabra.fi/wiki/uploads/upload_cea18ad3bb898d9b679ef61592c09fff.png)


Seuraavaksi tehdään bin kellonajoille joka df.groupby komennolla yhdistetään dataframessa oleviin aloitusaikoihin. Otetaan myös ajoista keskiarvot.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_57b5ff66bdcbdd51459ce77f231c49ed.png)


Sitten voidaan rueta plottaamaan läpimenoajoista plotteja. Järkevin plotattava on tietysti keskiaika aina tiettyihin kellonaikoihin

![](https://gitlab.dclabra.fi/wiki/uploads/upload_9cae9757dd39be962de3e63415a214d8.png)

Tässä näemme että eniten aikaa vietetään kaupassa klo 17-19 välissä mikä on ymmärrettävää sillä tähän aikaan ihmiset pääsevät töistä ja käyvät sitten työpäivän päätteeksi kaupassa.



Seuraavaksi otetaan talteen viikonpäivät sekä laitetaan ne oikeaan järjestykseen sillä alunperin ne ovat aivan satunnaisessa järjestyksessä.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_004ecdb597000613f63ad02709dc3487.png)


Sitten vielä viikonpäiville sama keskiarvojen plottaus. Plottasin myös kokonaisajat joka päivälle mutta ne tuntuvat aika turhilta keskiarvoihin verrattuna.

![](https://gitlab.dclabra.fi/wiki/uploads/upload_c52bcbd6139919f283c7748b7026203a.png)

Tässä plottauksessa sitten yllättävämmin näkyy että eniten kaupassa vietetään keskimäärin aikaa tiistaisin. Tässä plottaukset ovat kuitenkin todella tasaisia ja plottauksen yläpuolella näkyykin pyöristetyt arvot kaupassakäyntien ajoista mistä näemme että 8 minuuttia on yleisin arvo.
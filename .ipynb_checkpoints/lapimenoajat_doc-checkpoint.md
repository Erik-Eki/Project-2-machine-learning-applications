#### Läpimenoajat dokumentointi

Ensin ohjelmoidaan luokka jossa on kärrit/korit ja timestamppien avulla saadaan tehtyä niistä lista. Tässä listassa on korien/kärryjen node_id:t, timestampit sekä koordinaatit. Näitten avulla voidaan katsoa muutokset kyseisissä muuttujissa ja näiden avulla määritellä ajokerrat.
![](https://notebooks.dclabra.fi/user/kostikaa/files/Projekti2/projekti-2-team-fox/Screenshot_1.png?_xsrf=2%7Ca9b721a3%7Cd246370ae9d9bcc15b37bc7924559e7e%7C1605853961)

Tämän jälkeen otetaan timestamppien perusteella joka ajokerran läpimenoaika.

![](https://notebooks.dclabra.fi/user/kostikaa/lab/tree/Projekti2/projekti-2-team-fox/Screenshot_2.png)

Tallennetaan kyseiset läpimenoajat sekä aloitus ajat listaan mikä 
sitten tallennetaan dataframeen. Tähän kannattaa tehdä uusi dataframe. 

![](https://notebooks.dclabra.fi/user/kostikaa/lab/tree/Projekti2/projekti-2-team-fox/Screenshot_3.png)

Seuraavaksi tehdään bin kellonajoille joka df.groupby komennolla yhdistetään dataframessa oleviin aloitusaikoihin. Otetaan myös ajoista keskiarvot.

![](https://notebooks.dclabra.fi/user/kostikaa/lab/tree/Projekti2/projekti-2-team-fox/Screenshot_4.png)

Sitten voidaan rueta plottaamaan läpimenoajoista plotteja. Järkevin plotattava on tietysti keskiaika aina tiettyihin kellonaikoihin

![](https://notebooks.dclabra.fi/user/kostikaa/lab/tree/Projekti2/projekti-2-team-fox/Screenshot_5.png)

Seuraavaksi otetaan talteen viikonpäivät sekä laitetaan ne oikeaan järjestykseen sillä alunperin ne ovat aivan satunnaisessa järjestyksessä.

![](https://notebooks.dclabra.fi/user/kostikaa/lab/tree/Projekti2/projekti-2-team-fox/untitled.md)

Sitten vielä viikonpäiville sama keskiarvojen plottaus. Plottasin myös kokonaisajat joka päivälle mutta ne tuntuvat aika turhilta keskiarvoihin verrattuna.

![](https://notebooks.dclabra.fi/user/kostikaa/lab/tree/Projekti2/projekti-2-team-fox/Screenshot_7.png)

### Ajamalla clean_dataframe funktion tapahtuu seuraavaa:

- Muuttuja ottaa dataframen sisään
- Aluksi vaihtaa pandasin factorize:lla node_id:n arvon pitkästä tekstirimpsusta arvoihin 1, 2, 3.. niin moneen kuin dataframessa eri node_id:itä löytyy
- Seuraavaksi se muokkaa timestamp muuttujan datetime muotoon
- Pyöristää timestampin millisekuntin tarkkuuteen
- Laittaa aikavyöhykkeen aikavyöhykkeeksi Helsingin
- Pudottaa +00 lopun timestampista
- Seuraavaksi se poistaa kaupan ulkopuolella olevan datan, eli normaaliarkena 8-21 ulkopuolella olevat ja sunnuntaisin 10-21 ulkopuolella olevat
- Lopuksi pudotetaan kolumnit 'z' ja 'q'

### Yhteenveto

- Muuttuja siis poistaa turhat kolumnit, z ja q, muokkaa aikaleiman oikeaan muotoon ja pudottaa arvot jotka eivät ole kaupan aukioloajan sisällä


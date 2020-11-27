### Ajamalla clean_dataframe funktion tapahtuu seuraavaa:

- Muuttuja ottaa dataframen sisään

-Aluksi muodossa: 

![](https://gitlab.dclabra.fi/wiki/uploads/upload_2c0f02e6e254165134ec4789024372c4.png)

- Aluksi vaihtaa pandasin factorize:lla node_id:n arvon pitkästä tekstirimpsusta arvoihin 1, 2, 3.. niin moneen kuin dataframessa eri node_id:itä löytyy:

```python=
df['node_id'] = pd.factorize(df['node_id'])[0] + 1
```


- Seuraavaksi se muokkaa timestamp muuttujan datetime muotoon


```python=
# Timestamp to datetime
df['timestamp'] = df['timestamp'].astype(str)
df['timestamp'] = df['timestamp'].str.slice(2, -7)
df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
```


- Pyöristää timestampin millisekuntin tarkkuuteen

`df.timestamp = df.timestamp.dt.round("ms")`


- Laittaa aikavyöhykkeen aikavyöhykkeeksi Helsingin

```python=
df.timestamp = df.timestamp.dt.tz_localize('UTC')

# Muunnetaan Suomen aikaan. Tämä huomioi kesä- ja talviajan.
df.timestamp = df.timestamp.dt.tz_convert('Europe/Helsinki')
```


- Pudottaa +00 lopun timestampista

```python=
df['timestamp'] = df['timestamp'].astype(str)
df['timestamp'] = df['timestamp'].str.slice(0, -7)
df['timestamp'] = df['timestamp'].astype('datetime64[ns]')
```

- Seuraavaksi lisätään viikonpäiväkolumni:

```
df['dayofweek'] = df.timestamp.dt.dayofweek
```


- Seuraavaksi se poistaa kaupan ulkopuolella olevan datan, eli normaaliarkena 8-21 ulkopuolella olevat ja sunnuntaisin 10-21 ulkopuolella olevat

```python=
df = df.drop(df[(df.timestamp.dt.hour < 8)].index) #dropataan kaikki 8-21 ulkopuolella olevat tunnit
df = df.drop(df[(df.timestamp.dt.hour > 21)].index)
df = df.reset_index(drop=True) # resetoidaan indexit, että voidaan ajaa uudet koodit

df_temp = df[df.timestamp.dt.dayofweek == 6].index.values.tolist()
df_new_temp = df.iloc[df_temp][df.iloc[df_temp].timestamp.dt.hour < 10]

df = df.drop(df.index[df_new_temp.index.values])
    
df = df.reset_index(drop=True)
```


- Sen jälkeen lisätään uusi kolumni, current_hour
- Tämä sisältää tunnin milloin ollaan kaupassa, esim klo 8 on ensimmäinen tunti, 9 on toinen jne. kolumni muodossa int
- Kolumni luodaan seuraavalla tavalla:

 ```python=

#alustetaan uusi kolumni nollalla, tähän tulee kyseinen tunti kaupassa, esimerkiksi klo 8 eli aukioloajan ensimmäinen tunti on 1
df['current_hour'] = 0
# Käydään läpi timestamp ja jokaikisen tunnin kohdalle lisätään yksi tunti. Aloitetaan tunnista 8
#Koska 8-21 välillä 15 tuntia, ajetaan tämä 15 kertaa
for i in range(15):
    
    df['current_hour'].loc[df['timestamp'].dt.hour == 8+i] = 
#Sunnuntaina aloitetaan kaksi tuntia myöhemmin, joten vähennetään kaksi tuntia jokaisesta hetkestä
df['current_hour'].loc[df['timestamp'].dt.dayofweek == 6] = df['current_hour'].loc[df['timestamp'].dt.dayofweek == 6] - 2
    
```





- Lopuksi pudotetaan kolumnit 'z' ja 'q'


`df = df.drop(columns=['z','q'])`




### Yhteenveto

- Muuttuja siis poistaa turhat kolumnit, z ja q, muokkaa aikaleiman oikeaan muotoon ja pudottaa arvot jotka eivät ole kaupan aukioloajan sisällä

-Lopputulos jotakin tällaista:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_a0cf131f7592a669612247cbc2780f0a.png)


# Write_df_to_database

Moduuli ottaa sisään dataframen

## 1. Tietokanta (MariaDB) Yhteys


```python
import mysql.connector
mydb = mysql.connector.connect(
host="172.28.200.50",
user="root",
port=3306,
passwd="insert-password-here",
database="iiwari_org")

# create new table to mariadb-server
mycursor = mydb.cursor(dictionary=True)
```
## 2. Taulun luominen tietokantaan -> TODO: Laita omaan moduuliin
*mycursor.execute*:lla voidaan suorittaa tietokantaan sql kyselyjä. Mennään halutun tietokannan sisälle ja luodaan sinne uusi TAULU muotoa:



|          | node_id | timestamp | x   |y  | x_grid|y_grid |grid_id|
| -------- | -------- | -------- | ----|---|---|---|---|
| 0     |      |      | |||


```python
mycursor.execute("USE iiwari_org;");
mycursor.execute("DROP TABLE IF EXISTS CleanSensorData;");
mycursor.execute("CREATE TABLE CleanSensorData (node_id INTEGER NOT NULL,timestamp TEXT,x INTEGER NOT NULL,y INTEGER NOT NULL,x_grid INTEGER NOT NULL,y_grid INTEGER NOT NULL,grid_id INTEGER NOT NULL);");
```

## 3. Dataframen kirjoittaminen tehtyyn tauluun sqlalchemyllä -> TODO: Tee chunkit dataframen jakamiseen


### 3.1 Luodaan sqlalchemy engine johon parametreina laitetaan sql-servun user, password ja host(ip)

```python
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:insert-password-here@172.28.200.50/iiwari_org')
```


### 3.2 Kirjoitetaan dataframe osissa tietokantaan. -> TODO: Muunnos CHUNKEIKSI

Liian ison määrän kirjoittaminen aiheuttaa aikakatkaisun (Connection-reset-by-peer), siksi joudumme osissa kirjottamaan


enkä jaksa dokumentoida tätä mutta jos dataframe on tarpeeksi pieni niin saadaan se menemään kyseisellä komennolla, jossa
- 'CleanSensordData' = tietokannassa oleva taulu mihin data tungetaan
- con = **3.1**:ssä tehty *engine*
- if_exist = mitä tehdään jos taulu on olemassa.
- index = Halutaanko dataframen indeksointi mukaan

```df.to_sql('CleanSensorData', con = engine, if_exists = 'append',index = False)```
```python
x = 0
y = 200000

for i in range(int(len(df)/y+1)):
    df[x:x+y].to_sql('CleanSensorData', con = engine, if_exists = 'append',index = False)
    x += y
```
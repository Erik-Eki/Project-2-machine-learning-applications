# Database connection

Tämä siis toimii ainakin mariaDB tietokantaan. 
### Tarvittavat kirjastot:
```python
import pandas as pd
import mysql.connector
```

### Mysql-connectorin asetukset:
- host = Mysql-servun ip-osoite
- user = Mysql-servun käyttäjä, esim root
- port = Portti jota mysql-servu kuuntelee
- passwd = Mysql-käyttäjän salasana
- database = Haluttu tietokanta

Tehdään tästä funktio joka ottaa sisälleen sql kyselyn esim. ***"Select * From Sensordata"***
```python
def database_query(sql_query):

    mydb = mysql.connector.connect(
      host="172.28.200.50",
      user="root",
      port=3306,
      passwd="insert-password-here",
      database="iiwari_org")
```

### Mysql-connectorin mycursor objekti
- mydb.cursor = saadaan valittua tietokanta
- mycursor.execute = saadaan suoritettua haluttu sql kysely

Otetaan dataframeen haettu data **.fetchall()** toiminnolla

```python
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql_query);

    df = pd.DataFrame(mycursor.fetchall())
    return df
```

blablablaa juuhaa
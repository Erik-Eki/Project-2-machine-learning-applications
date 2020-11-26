
# Write_df_to_database

## 1. Tietokanta (MariaDB) Yhteys

Funktio ottaa sisään dataframen ja taulun nimen: ```write_df_to_database(df, 'Taulu')```

Funktio luo uuden tai kysyy dropataanko olemassa oleva taulu.

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
## 2. Tarkistetaan onko taulu jo tietokannassa

Jos taulu löytyy tietokannasta niin palauttaa kyselyn, jossa kysytään varmistusta olemassa olevan taulun poistamisesta.

Muuten jatkaa ilman varmistusta.


```python
try:
        mycursor.execute("DROP TABLE IF EXISTS {};".format(table))
        print("Existing table found. Prepairing to Drop Table named {}...".format(table))
        
        while True: 
            confirm = input('Continue? yes/no: ')

            if confirm == 'yes' or confirm == 'y':
                break;
            elif confirm == 'no' or confirm == 'n':
                return print('Aborting...')
            else:
                print("Invalid input. Try again")
        
    except ReferenceError:
        print("No existing table named {} found. Writing started...".format(table)) 
```

## 3. Dataframen kirjoittaminen tietokantaan

Ensiksi tehdään sqlalchemyn vaatima engine(tietokantayhteys).
Tehdään dataframesta 200 000 rivin kokoisia chunkkeja jotka sitten syötetään annettuun tauluun.

Taulusta tulee samaa muotoa kuin dataframesta eli sarakkeiden mukaan.

```python
    # mysql engine init
    engine = create_engine('mysql+mysqlconnector://root:insert-password-here@172.28.200.50/iiwari_org')
    
    print("Done! Prepairing to write dataframe to {}".format(table))

    # Kirjoitetaan osissa koko dataframe koska tulee muuten yhteyden aikakatkaisu
    n = 200000  # chunk size
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]

    for i in range(len(list_df)):
        list_df[i].to_sql(table, con = engine, if_exists = 'append',index = False)
        print('Writing data', i+1, '/', len(list_df))
    
    print("Done!")
```


import pandas as pd
from sqlalchemy import create_engine

# dataframen columnit = node_id timestamp x y
def write_df_to_mariadb(df):
    

        #Timestamp muodossa 2020-06-01 06:00:10.968
        #df['timestamp'] = df['timestamp'].astype(str)
        #df['timestamp'] = df['timestamp'].str.slice(0, -7)
        #df['timestamp'] = df['timestamp'].astype('datetime64[ns]')

    # mariadb connection
    import mysql.connector
    mydb = mysql.connector.connect(
    host="172.28.200.50",
    user="root",
    port=3306,
    passwd="insert-password-here",
    database="iiwari_org")

    # create new table to mariadb-server
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("USE iiwari_org;");
    mycursor.execute("DROP TABLE IF EXISTS CleanSensorData;");
    mycursor.execute("CREATE TABLE CleanSensorData (node_id INTEGER NOT NULL,timestamp TEXT,x INTEGER NOT NULL,y INTEGER NOT NULL,xy_grid DOUBLE NOT NULL);");

    # mysql engine init
    engine = create_engine('mysql+mysqlconnector://root:insert-password-here@172.28.200.50/iiwari_org')

    # Kirjoitetaan osissa koko dataframe koska tulee muuten yhteyden aikakatkaisu
    x = 0
    y = 200000

    for i in range(int(len(df))/y+1):
        df[x:x+y].to_sql('CleanSensorData', con = engine, if_exists = 'append',index = False)
        x += y
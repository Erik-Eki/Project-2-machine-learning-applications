import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

def write_df_to_mariadb(df, table):
    """
    --------------------------------------
    Takes 2 arguments:
    - dataframe
    - table name for database
    ---------------------------------------
    If table exist: Drop table from database
    
    else: Starts writing dataframe to database
    --------------------------------------
    Table columns and types are automatically created based on
    dataframe columns and their types.
    --------------------------------------
    """
    mydb = mysql.connector.connect(
      host="172.28.200.50",
      user="root",
      port=3306,
      passwd="insert-password-here",
      database="iiwari_org")


    mycursor = mydb.cursor(dictionary=True)
    
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
    
    # mysql engine init
    engine = create_engine('mysql+mysqlconnector://root:insert-password-here@172.28.200.50/iiwari_org')
    
    print("Done! Prepairing to write dataframe to {}".format(table))

    # Kirjoitetaan osissa koko dataframe koska tulee muuten yhteyden aikakatkaisu
    n = 200000  # chunk size
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]

    for i in range(len(list_df)):
        list_df[i].to_sql(table, con = engine, if_exists = 'append',index = False)
        print('Writing data', i+1, '/', len(list_df))
    
    mycursor.close()
    mydb.close()
    print("Done!")
    


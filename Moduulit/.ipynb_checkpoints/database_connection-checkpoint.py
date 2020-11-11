import pandas as pd
import mysql.connector

def database_query(sql_query):

    mydb = mysql.connector.connect(
      host="172.28.200.50",
      user="root",
      port=3306,
      passwd="insert-password-here",
      database="iiwari_org")


    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql_query);

    df = pd.DataFrame(mycursor.fetchall())
    return df
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
from database_connection import *
import ipywidgets as widgets
import pandas as pd


OptTables = database_query("SHOW Tables;")
OptTables = OptTables.Tables_in_iiwari_org.values
 # Tunnit widgettien vaihtoehdoiksi
OptHours = list(range(8, 23))

 # Nodeidt listaan
nodeIds = []
nodeIds.append("All") 
for i in range(32):
    nodeIds.append(i+1)


start_date=widgets.DatePicker(value=pd.to_datetime('2020-05-01'),description='Starting Date', layout=Layout(margin='0px 0px 0px 0px'))                    
end_date=widgets.DatePicker(value=pd.to_datetime('2020-11-01 23:00:00'),description='Ending Date')

tunnit = widgets.SelectionRangeSlider(options=list(range(8, 23)),index=[0,14], description='Tunnit'
                                 ,disabled=False,value=[8,22])


def sort_by_widgets(df,start_date=start_date,end_date=end_date,tunnit=tunnit):
    
    # Sortaa pvm:s
    df = df.loc[df["timestamp"] >= pd.to_datetime(start_date.value)]
    df  = df.loc[df["timestamp"] < pd.to_datetime(end_date.value)]

    # Sorttaa tunnit                   
    df = df.loc[df.timestamp.dt.strftime('%-H').astype('int32') >= tunnit.value[0]]
    df = df.loc[df.timestamp.dt.strftime('%-H').astype('int32') < tunnit.value[1]]
    
    return df
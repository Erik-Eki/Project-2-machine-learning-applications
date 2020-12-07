df3 = df['timestamp']
df4 = df1['timestamp']
#df[df['timestamp'].isin(df1['timestamp'])]
df5 = df4[~df4.isin(df3)].dropna()
df5

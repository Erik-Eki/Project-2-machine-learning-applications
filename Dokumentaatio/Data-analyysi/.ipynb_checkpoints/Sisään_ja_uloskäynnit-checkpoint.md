# Moduuli sisään- ja uloskäynnit

- Moduuli käyttää kahta kirjastoa: matplotlib.pyplot ja matplotlibin colors
- Moduuli sisältää neljä eri funktiota
- Ensimmäinen funktio on sisäänkäynnin tekeminen
- Funktio ottaa sisälle pandasin dataframen(jossa on jo valmiiksi x_grid ja y_grid)
- Tämän tekemisen voit katsoa kyseisen moduulin dokumentaatiosta
- dataframe näyttää jotakuinkin tältä:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_e3614a5721bf3bc2a664df0c58c0ec6e.png)


- Aluksi funktio ottaa gridin koon

```grid_size = max(df.x_grid)+1``` 

- Seuraavaksi se ottaa gridistä neliön muotoisen alueen: 

```
    min_x = 0.6 * grid_size
    max_x = 0.8 * grid_size
    min_y = 0 * grid_size
    max_y = 0.35 * grid_size


```

- Tämä alue on katsottu silmämääräisesti aiemmin tehdyistä plottauksista

- Lopuksi se määrittää  sisäänkäynnille alueen:

```
sisään_x = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].x_grid
sisään_y = df.loc[df.x_grid>=min_x].loc[df.x_grid<=max_x].loc[df.y_grid>=min_y].loc[df.y_grid<=max_y].y_grid
    
```

- Ja palauttaa kyseien alueen

- Seuraava funktio tekee Käytännössä täysin saman asian, siinä on vain määritelty eri alue:

```
    min_x = 0.3 * grid_size
    max_x = 0.5 * grid_size
    min_y = 0.2 * grid_size
    max_y = 0.35 * grid_size

```

- Sitten sisään ja uloskäyntejen piirtofunktio draw_exits():
- Ottaa seuraavat asiat sisään:
- dataframen, jossa on jo määritelty gridit
- Aiemmissa funktioissa määritellyt alueet, eli sisään_x, sisään_y, ulos_x, ulos_y
- Aluksi funktio plottaa x_gridin ja y_gridin pisteet, eli kaikki datframen x ja y pisteet

```
plt.hist2d(df['x_grid'], df['y_grid'], bins = 100, norm = colors.LogNorm())
```


- Seuraavaksi se plottaa Sisään ja uloskäynnin alueet:

```
plt.hist2d(sisään_x, sisään_y, bins = 100, norm=colors.LogNorm(),cmap="cool", label="Sisäänkäynti")
plt.hist2d(ulos_x, ulos_y, bins = 100, norm=colors.LogNorm(),cmap="spring", label="Kassat")
```

- Lopuksi skaalataan sisäänkäynnit koko kuvaan ja plotataan lopputulos:

```
plt.grid()
    
plt.show()

```

![](https://gitlab.dclabra.fi/wiki/uploads/upload_2a39f7b5c130ce6e8de53c356ace11b0.png)


- Viimeisenä funktiona xy_to_ID
- funktio ottaa sisälleen gridin x ja y koordinaatit
- Ja gridin koon millä se on luotu
- Palauttaa gridin koon mukaan muokatun ID:n

```
ID = grid_size*y+x
    return ID

```
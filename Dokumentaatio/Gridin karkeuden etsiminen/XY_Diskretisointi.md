# XY_DISKRETISOINTI

Moduuli ottaa sisään *dataframen*, *x*, *y* ja halutun gridin karkeisuuden *k*

## 1. Jaetaan x ja y arvot yhtäsuuriin osiin

Pandasin cut-funktiolla saadaan halutut arvot yhtäsuuriin osiin, joiden määrä riippuu arvosta *k* eli jos meillä ```x= [1,2,3,4,5,6,7,8,9,10]``` , ```y= [1,2,3,4,5,6,7,8,9,10]``` ja halutaan gridiksi 2x2 nii laitetaan ```k=2``` jolloin x ja y arvot jakautuu kahteen osaan: ```x=([1,2,3,4,5], [6,7,8,9,10])``` ja ```y=([1,2,3,4,5], [6,7,8,9,10])```


## 2. Laitetaan saadut arvot dataframeen
```python
df['x_grid'], df['y_grid'] = x_cut.values, y_cut.values
```

## 3. Luodaan grid_id dataframeen

Kaava on siis ```grid_id = y_grid * gridinkarkeisuus + x_grid```

```python
df['grid_id'] = df['y_grid'] * k + df['x_grid']
```

esim 5x5 gridi indeksoituna
```
__________________________
| 20 | 21 | 22 | 23 | 24 |
| 15 | 16 | 17 | 18 | 19 |
| 10 | 11 | 12 | 13 | 14 |
| 5  | 6  | 7  | 8  | 9  |
| 0  | 1  | 2  | 3  | 4  |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

# Kassa-alueet

- Tutkittiin, kuinka monta kassaa mahdollisesti kassassa on.
- Aluksi silmämääräisesti tutkittuamme saimme piirrettyä kassa-alueen.

```
in_x, in_y = sisään(df, 'x', 'y')
out_x, out_y = ulos(df, 'x', 'y')

draw_exits(df, in_x, in_y, out_x, out_y, 'x', 'y')

```

![](https://gitlab.dclabra.fi/wiki/uploads/upload_55df849bd651c9694f0e7d844d45ee29.png)


- Kuten kuvasta näkyy, x-koordinaattejen 1500 ja 2000 välillä olevaan kohtaan muodostuu kassa-alue
- Seuraavaksi plottasin yhden päivän datan puolista nodeista:

![](https://gitlab.dclabra.fi/wiki/uploads/upload_b07d6a26445ad4626f622d26b302e8d5.png)

![](https://gitlab.dclabra.fi/wiki/uploads/upload_6ef7853b4aee4e81bdcb3733f5312ecf.png)


- Kuten huomataan, kassojen alueelle muodostuu kolme ns. pallorypästä
- Tästä päätellään, että kaupassa on kolme kassaa.
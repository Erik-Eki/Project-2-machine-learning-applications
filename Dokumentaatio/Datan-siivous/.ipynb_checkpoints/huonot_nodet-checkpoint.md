# Huonot nodet


- Tarkasteltuamme kaikkien eri nodejen dataa ja piirrettyämme niistä plotit, huomaamme, että osa tageista on selvästi rikki, joten poistamme ne datasta
- Huonot nodet ovat, 13, 14, 18, 27,  32

![](https://gitlab.dclabra.fi/wiki/uploads/upload_81920d1b5030ee2e97895e28a6480674.png)

![](https://gitlab.dclabra.fi/wiki/uploads/upload_ddb08e983ec8a8dc91fd10a30858023a.png)


![](https://gitlab.dclabra.fi/wiki/uploads/upload_2fd43017df1ce79e65c0c11f36fffdd2.png)

![](https://gitlab.dclabra.fi/wiki/uploads/upload_451c3f81b5460db3da4a13b46bf5846e.png)

![](https://gitlab.dclabra.fi/wiki/uploads/upload_6f677d03235b345bf5f2fde4e2832f5a.png)

- Joten näitä nodeja ei voi hyödyntää data-analyyseissä ja siksi ne on helpoin poistaa datasetistä

```
df1 = df1[df1.node_id != 13]
df1 = df1[df1.node_id != 14]
df1 = df1[df1.node_id != 18]
df1 = df1[df1.node_id != 27]
df1 = df1[df1.node_id != 32]


```

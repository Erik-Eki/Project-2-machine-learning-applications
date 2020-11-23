def draw_node_amount(df, column):
    # Kopioidaan taulu
    dftest = df.copy()
    # Alustetaan Counter
    _count = Counter()
    # Annetaan Counterille node_id kolumni
    _count.update(dftest[column])

    cart_name = []
    cart_amount = []

    #Täytetään listat noden nimellä ja lasketaan kuinka monta kertaa kyseinen node esiintyy taulussa
    for i in _count:
        #print('%s : %d' % (i, _count[i]))
        cart_name.append(i)
        cart_amount.append(_count[i])

    #Järjestetään node_id:t
    y_pos = np.arange(len(cart_name))

    N = 20
    cmap = cm.tab20(np.linspace(0, 1, N))
    plt.figure(figsize=(10, 7))

    line = plt.barh(y_pos, cart_amount, color=cmap)
    plt.yticks(y_pos, cart_name)
    plt.xlabel('Määrä')
    plt.title('Nodejen käyttömäärä')

    # Lisätään palkkien perään palkin pituus.
    for p in line.patches:
        width = p.get_width()
        plt.text(5+p.get_width(), p.get_y()+0.55*p.get_height(),
                 '{:1.2f}'.format(width), va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig("Nodejen käyttömäärä.png")
    plt.show()
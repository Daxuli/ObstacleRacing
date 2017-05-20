def rock(fila, estado, start, tiempo):
    parpadea = estado[0]
    if parpadea != 0 and tiempo:
        estado[0] += 1
        if parpadea == 3:
            estado[0] = 0
    elif parpadea == 0 and fila < 19:
        fila += 1
        estado[0] += 1
    elif parpadea == 0:
        fila += 1
        start = False

    return fila, estado, start


def beer(columna, filamapa, estado, tiempo):
    if filamapa[columna] == 2:
        filamapa[columna] = 0
        estado[1] = 1
    if tiempo:
        estado[1] += 1
        if estado[1] == 7:
            estado[1] = 0
    return filamapa, estado


def coin(columna, filamapa, estado):
    filamapa[columna] = 0
    estado[2] += 1
    return filamapa, estado


def octopus(columna, filamapa, estado, tiempo):
    if filamapa[columna] == 4:
        filamapa[columna] = 0
        estado[3] = 1
    if tiempo:
        estado[3] += 1
        if estado[3] == 7:
            estado[3] = 0
    return filamapa, estado


def tirachinas(columna, filamapa, estado, tiempo):
    if filamapa[columna] == 5:
        filamapa[columna] = 0
        estado[4] = 1
    if tiempo:
        estado[4] += 1
        if estado[4] == 13:
            estado[4] = 0
    return filamapa, estado


if __name__ == "__main__":
    fila, estados = rock(15, [3, 0, 0, 0, 0], True)
    print(fila)
    print(estados)
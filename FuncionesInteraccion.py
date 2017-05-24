def rock(fila, estado, start, tiempo):
    """
    El coche choca con la roca y es arrastrado hacia abajo. Si sale de la pantalla, pierde el jugador
    Durante los tres segundos siguientes se vuelve inmuna a nuevas rocas
    :param fila: fila en la que se encuentra el jugador
    :param estado: indice 0 indica el tiempo que lleva parpadeando el jugador
    :param start: valor de juego en ejecucion del jugador
    :param tiempo: clasificador de quien ha llamado a la funcion
    """
    parpadea = estado[0]
    if parpadea != 0 and tiempo:  # caso 1: al pasar un segundo se suma al estado una unidad hasta llegar a 3
        estado[0] += 1
        if parpadea == 3:
            estado[0] = 0
    elif parpadea == 0 and fila < 19:  # caso 2: se choca con la roca sin estar en la fila 20
        fila += 1
        estado[0] += 1
    elif parpadea == 0:  # caso 3: se choca con la roca en la fila 20. El jugador pierde y se para la partida
        fila += 1
        start = False

    return fila, estado, start


def beer(columna, filamapa, estado, tiempo):
    """
    El coche choca con la cerveza y se invierten los mandos
    Si se choca de nuevo con otra cerveza, se resetea el contador
    :param columna: indice de la columna de la cerveza
    :param filamapa: array de la fila en la que se encuentra
    :param estado: indice 1 indica el tiempo que lleva borracho el jugador
    :param tiempo: clasificador de quien ha llamado a la funcion
    """
    if filamapa[columna] == 2:  # caso 1: si se acaba de chocar, desaparece la cerveza del mapa y pone el contador en 1
        filamapa[columna] = 0
        estado[1] = 1
    elif tiempo:   # caso 2: al pasar un segundo se suma al estado una unidad hasta llegar a 7
        estado[1] += 1
        if estado[1] == 7:
            estado[1] = 0
    return filamapa, estado


def coin(columna, filamapa, estado, start):
    """
    El coche choca coge una nueva moneda
    Si el jugador coge 10 monedas, gana la partida
    :param columna: indice de la columna de la moneda
    :param filamapa: array de la fila en la que se encuentra
    :param estado: indice 2 indica el numero de monedas que lleva el jugador
    :param start: valor de juego en ejecucion del jugador    
    """
    filamapa[columna] = 0  # quita la moneda del mapa
    estado[2] += 1
    if estado[2] == 10:
        start = False
    return filamapa, estado, start


def octopus(columna, filamapa, estado, tiempo):
    """
    El coche choca con el pulpo y deja de ver las filas superiores
    Si se choca de nuevo con otro pulpo, se resetea el contador
    :param columna: indice de la columna del pulpo
    :param filamapa: array de la fila en la que se encuentra
    :param estado: indice 3 indica el tiempo que lleva cegado el jugador
    :param tiempo: clasificador de quien ha llamado a la funcion
    """
    if filamapa[columna] == 4:  # caso 1: si se acaba de chocar, desaparece el pulpo del mapa y pone el contador en 1
        filamapa[columna] = 0
        estado[3] = 1
    elif tiempo:  # caso 2: al pasar un segundo se suma al estado una unidad hasta llegar a 7
        estado[3] += 1
        if estado[3] == 7:
            estado[3] = 0
    return filamapa, estado


def tirachinas(columna, filamapa, estado, tiempo):
    """
    El coche lanza piedras hacia el otro jugador durante 12 segundos
    Si se choca de nuevo con otro tirachinas, se resetea el contador
    :param columna: indice de la columna del tirachinas
    :param filamapa: array de la fila en la que se encuentra
    :param estado: indice 4 indica el tiempo que lleva recibiendo pedradas el jugador(estado del otro jugador)
    :param tiempo: clasificador de quien ha llamado a la funcion
    """

    if filamapa[columna] == 5:  # caso 1: si se acaba de chocar, desaparece el objeto del mapa y pone el contador en 1
        filamapa[columna] = 0
        estado[4] = 1
    elif tiempo:  # caso 2: al pasar un segundo se suma al estado una unidad hasta llegar a 13
        estado[4] += 1
        if estado[4] == 13:
            estado[4] = 0
    return filamapa, estado


if __name__ == "__main__":
    print("rock", end=": ")
    fila, estados, start = rock(15, [0, 0, 0, 0, 0], True, True)
    print(fila, estados, start)

    print("beer", end=": ")
    filamapa, estados = beer(4, [1, 1, 1, 1, 2, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0], True)
    print(filamapa, estados)

    print("coin", end=": ")
    filamapa, estados = coin(4, [1, 1, 1, 1, 3, 0, 1, 1, 1, 1], [0, 0, 3, 0, 0], True)
    print(filamapa, estados)

    print("octopus", end=": ")
    filamapa, estados = octopus(4, [1, 1, 1, 1, 4, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0], True)
    print(filamapa, estados)

    print("tirachinas", end=": ")
    filamapa, estados = tirachinas(4, [1, 1, 1, 1, 2, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0], True)
    print(filamapa, estados)
import random
import numpy as np
import TypeChecker as TC


def randomarray(maps):
    """
    Genera una nueva fila aleatoriamente
    :param maps: array de matrices de objetos
    """
    lista = np.zeros(10, dtype=int)
    if not(any(maps[0][0]) or any(maps[0][1])):  # si las primeras dos filas son de ceros
        for i in range(10):
            val = random.randint(0, 19)
            if val < 4:
                lista[i] = 0  # vacio
            elif val < 16:
                lista[i] = 1  # rock
            elif val == 16:
                lista[i] = 2  # beer
            elif val == 17:
                lista[i] = 3  # coin
            elif val == 18:
                lista[i] = 4  # octopus
            elif val == 19:
                lista[i] = 5  # tirachinas
        if not (any(np.where(lista == 0)[0])):  # Si no hay ningun 0, se lo asigna a una posicion aleatoria
            val = random.randint(0, 9)
            lista[val] = 0
    return lista


def tirachinasarray(linea, estado):
    """
    Sustituye un 0 por una piedra si el jugador esta recibiendo pedradas
    :param linea: linea generada en @randomarray
    :param estado: lista de estados del jugador
    :return: 
    """
    if estado[4] != 0 and any(linea):  # si la linea no esta vacia
        indices = np.where(linea == 0)[0]
        linea[random.choice(indices)] = 1
    return linea


def gameloop(data):
    """
    Funcion principal que llama @PeriodicCallback
    Actualiza las matrices de los mapas, calcula las interacciones y envia a los clientes la nueva info
    :param data: todos los datos de los clientes
    :return: 
    """
    start = data['start']
    maps = data["map"]
    connections = data['conn']
    position = data['pos']
    status = data['stat']
    # if all(start) and start:  # all de un array vacio va a dar True porque no hay ningun False
    if start == [True, True]:  # condición orientada al caso de 2 jugadores
        jugadores = len(maps)  # numero de jugadores
        line = np.array(randomarray(maps))
        lineas = []
        for i in range(jugadores):  # nuevos mapas
            lineas.append(line)
            lineas[i] = tirachinasarray(line, status[i])
            maps[i] = np.insert(maps[i], 0, lineas[i], axis=0)
            maps[i] = np.delete(maps[i], 20, axis=0)

        for i in range(jugadores):  # interacciones
            maps, position, status, start = TC.interaccion(i, maps, position, status, start, True)

        mapas = map(np.matrix.tolist, maps)  # convertimos cada matriz en una lista
        mapalista = []
        for elem in mapas:
            mapalista.append(elem)  # añadimos cada lista a una general:[[mapa1], [mapa2]]
        for elem in connections:  # envio de info
            i = connections.index(elem)
            elem.write_message({"index": i, "msg": position,
                                "map": mapalista, "stat": status})

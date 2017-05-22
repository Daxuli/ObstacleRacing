import random
import tornado.ioloop
import numpy as np
import TypeChecker as TC


def randomarray(maps):
    lista = np.zeros(10, dtype=int)
    if not(any(maps[0][0]) or any(maps[0][1])):
        for i in range(10):
            val = random.randint(0, 19)
            if val < 4:
                lista[i] = 0
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
        if not any(np.where(lista == 0)[0]):
            val = random.randint(0, 9)
            lista[val] = 0
    return lista


def tirachinasarray(linea, estado):
    if estado[4] != 0 and any(linea):
        indices = np.where(linea == 0)[0]
        linea[random.choice(indices)] = 1
    return linea

def gamechecker(posiciones, estados, start):
    for i in range(len(posiciones)):
        j = 0
        if i == 0:
            j = 1
        if estados[j][2] == 10:
            start[i] = False
    return start


def gameloop(data):
    start = data['start']
    maps = data["map"]
    connections = data['conn']
    position = data['pos']
    status = data['stat']
    if all(start) and start:  # all de un array vacio va a dar True porque no hay ningun False
        start = gamechecker(position, status, start)
        jugadores = len(maps)
        line = np.array(randomarray(maps))
        lineas = []
        for i in range(jugadores):
            lineas.append(line)
            lineas[i] = tirachinasarray(line, status[i])
            maps[i] = np.insert(maps[i], 0, lineas[i], axis=0)
            maps[i] = np.delete(maps[i], 20, axis=0)

        for i in range(jugadores):
            maps, position, status, start = TC.interaccion(i, maps, position, status, start, True)

        mapas = map(np.matrix.tolist, maps)  # convertimos cada matriz en una lista
        mapalista = []
        for elem in mapas:
            mapalista.append(elem)  # añadimos cada lista a una general:[[mapa1], [mapa2]]
        for elem in connections:
            i = connections.index(elem)
            elem.write_message({"index": i, "msg": position,
                                "map": mapalista, "stat": status})


if __name__ == "__main__":
    dict = {"start": [True, True], "map": [np.zeros((20, 10), dtype=int), np.zeros((20, 10), dtype=int)],
            "stat":[[0, 0, 0, 0, 2], [0, 0, 0, 0, 2]]}
    maps = dict["map"]
    print(not all(maps[0][0]))



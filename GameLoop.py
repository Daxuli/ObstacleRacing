import random
import numpy as np


def randomarray(maps):
    lista = [0]*10
    if not(any(maps[0][0]) or any(maps[0][1])):
        for i in range(10):
            val = random.randint(0, 19)
            if val < 4:
                lista[i] = 0
            elif val < 16:
                lista[i] = 1
            elif val == 16:
                lista[i] = 2
            elif val == 17:
                lista[i] = 3
            elif val == 18:
                lista[i] = 4
            elif val == 19:
                lista[i] = 5
        if not any(lista):
            val = random.randint(0, 9)
            lista[val] = 0
    return lista

def gameloop(data):
    start = data['start']
    if all(start) and start:  # all de un array vacio va a dar True porque no hay ningun False
        maps = data["map"]
        line = np.array(randomarray(maps))
        for i in range(len(maps)):
            maps[i] = np.insert(maps[i], 0, line, axis=0)
            maps[i] = np.delete(maps[i], 20, axis=0)
        print(maps[0])

if __name__ == "__main__":
    dict = {"start": [True, True], "map": [np.zeros((20, 10), dtype=int), np.zeros((20, 10), dtype=int)]}
    maps = dict["map"]
    #print(not all(maps[0][0]))
    gameloop(dict)


import random
import numpy as np

def randomarray():
    list = [0]*10
    for i in range(10):
        val = random.randint(0, 19)
        if val < 4:
            list[i] = 0
        elif val > 3 and val < 16:
            list[i] = 1
        elif val == 16:
            list[i] = 2
        elif val == 17:
            list[i] = 3
        elif val == 18:
            list[i] = 4
        elif val == 19:
            list[i] = 5
    if not any(list):
        val = random.randint(0, 9)
        list[val] = 0
    return list

def gameloop(data):
    start = data['start']
    if all(start) and start:  # all de un array vacio va a dar True porque no hay ningun False
        line = np.array(randomarray())
        maps = data["map"]
        for i in range(len(maps)):
            maps[i] = np.insert(maps[i], 0, line, axis=0)
            maps[i] = np.delete(maps[i], 20, axis=0)
        print(maps[0])

if __name__ == "__main__":
    dict = {"start": [True, True], "map": [np.zeros((20, 10), dtype=int), np.zeros((20, 10), dtype=int)]}
    gameloop(dict)


import FuncionesMensaje as FM
import FuncionesInteraccion as FI
import numpy as np


def check(i, mensaje, data):
    llave = []
    respuesta = data
    change = False
    for key in mensaje:
        llave.append(key)
    if llave[0] == "msg":
        respuesta, change = FM.fposicion(i, mensaje["msg"], data)

    if llave[0] == "go":
        respuesta, change = FM.fstart(i, data)
    return respuesta, change


def interaccion(i, mapas, posiciones, estados, tiempo):
    mapa = mapas[i]
    estado = estados[i]
    fila = posiciones[i][0]
    columna = posiciones[i][1]
    objeto = mapa[fila][columna]
    j = 1
    if i == 1:
        j = 0

    if objeto == 1 or estado[0] != 0:
        posiciones[i][0], estados[i] = FI.rock(fila, estado, tiempo)
    if objeto == 2 or estado[1] != 0:
        mapas[i][fila], estados[i] = FI.beer(columna, mapa[fila], estado, tiempo)
    if objeto == 3:
        mapas[i][fila], estados[i] = FI.coin(columna, mapa[fila], estado)
    if objeto == 4 or estado[3] != 0:
        mapas[i][fila], estados[i] = FI.octopus(columna, mapa[fila], estado, tiempo)
    if len(estados) == 2:
        if objeto == 5 or estados[j][4] != 0:
            mapas[i][fila], estados[j] = FI.tirachinas(columna, mapa[fila], estados[j], tiempo)
    return mapas, posiciones, estados


if __name__ == "__main__":
    midict = {"conn": [], "pos": [[14, 5], [14, 5]], "start": [True, False]}
    salidaP, cambio = check(0, {"msg": "L"}, midict)
    print(salidaP)
    print("---------------------------")

    salidaS, cambio = check(0, {"go": ""}, midict)
    print(all(salidaS["start"]))

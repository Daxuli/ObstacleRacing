"""
TypeChecker.py

Código que contiene 2 funciones: @check, @interaccion
y que relaciona a los siguientes módulos: @FuncionesMensaje, @FuncionesInteraccion
"""
import FuncionesMensaje as FM
import FuncionesInteraccion as FI
import numpy as np


def check(i, mensaje, data):
    """
    Clasifica el mensaje recibido por el cliente, y realiza las modificaciones oportunas
    :param i: identificador del cliente que ha enviado el mensaje
    :param mensaje: mensaje recibido
    :type mensaje: dict
    :param data: datos de todos los clientes
    :type data: dict

    :return cambio: devuelve si se han producido cambios a @ws o @GameLoop
    """
    llave = []
    respuesta = data
    change = False  # valor por defecto y definitivo si no se cumplen los siguientes condicionales
    for key in mensaje:  # convertimos la llave de @mensaje en un string que se guarda en la lista @llave
        llave.append(key)
    if llave[0] == "msg":  # input de L o R
        respuesta, change = FM.fposicion(i, mensaje["msg"], data)

    if llave[0] == "go":  # input de espacio
        respuesta, change = FM.fstart(i, data)
    return respuesta, change


def interaccion(i, mapas, posiciones, estados, start, tiempo):
    """
    Comprueba si el jugador esta en la misma casilla que otros objetos
    :param i: identificador del cliente
    :param mapas: array de matrices de objetos
    :param posiciones: array de posiciones de jugadores
    :param estados: array de estados de jugadores
    :param start: array de juego en ejecucion
    :param tiempo: clasificador de quien ha llamado a la funcion
    """
    mapa = mapas[i]
    estado = estados[i]
    fila = posiciones[i][0]
    columna = posiciones[i][1]
    objeto = mapa[fila][columna]
    j = 1  # empleado para el tirachinas, ya que modifica la lista de estados del otro cliente
    if i == 1:
        j = 0

    if objeto == 1 or estado[0] != 0:  # si choca con piedra o todavia sigue parpadeando
        posiciones[i][0], estados[i], start[i] = FI.rock(fila, estado, start[i], tiempo)
    if objeto == 2 or estado[1] != 0:
        mapas[i][fila], estados[i] = FI.beer(columna, mapa[fila], estado, tiempo)
    if objeto == 3:
        mapas[i][fila], estados[i], start[i] = FI.coin(columna, mapa[fila], estado, start[i])
    if objeto == 4 or estado[3] != 0:
        mapas[i][fila], estados[i] = FI.octopus(columna, mapa[fila], estado, tiempo)
    if len(estados) == 2:
        if objeto == 5 or estados[j][4] != 0:  # diferente al resto, coge la lista de estados del otro jugador
            mapas[i][fila], estados[j] = FI.tirachinas(columna, mapa[fila], estados[j], tiempo)
    return mapas, posiciones, estados, start


if __name__ == "__main__":
    midict = {"pos": [[14, 5], [14, 5]], "start": [True, False]}

    salidaS, cambio = check(1, {"go": "play"}, midict)
    print("check:", salidaS,"change:", cambio)

    salidaP, cambio = check(0, {"msg": "L"}, midict)
    print("check:", salidaP, "change:", cambio)
    print("---------------------------")

    mapas = [np.zeros((20, 10), dtype=int), np.zeros((20, 10), dtype=int)]
    mapas[0][14] = mapas[1][14] = [1, 1, 1, 1, 2, 0, 1, 1, 1, 1]
    estados = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    mapas, posiciones, estados, start = interaccion(0, mapas, midict["pos"], estados, midict["start"], True)
    print(mapas[0][14], posiciones, estados, start)

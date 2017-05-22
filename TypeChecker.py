"""
TypeChecker.py

Código que contiene 2 funciones: @check, @interaccion
y que relaciona a los siguientes módulos: @FuncionesMensaje, @FuncionesInteraccion
"""
import FuncionesMensaje as FM
import FuncionesInteraccion as FI


def check(i, mensaje, data):
    """
    Clasifica el mensaje recibido por el cliente, y realiza las modificaciones oportunas
    :param i: identificador del cliente que ha enviado el mensaje
    :param mensaje: mensaje recibido
    :type mensaje: dict
    :param data: datos de todos los clientes
    :type data: dict

    :return data: devuelve los nuevos datos a @ws o @GameLoop
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

    :param i:
    :param mapas:
    :param posiciones:
    :param estados:
    :param start:
    :param tiempo:
    :return:
    """
    mapa = mapas[i]
    estado = estados[i]
    fila = posiciones[i][0]
    columna = posiciones[i][1]
    objeto = mapa[fila][columna]
    j = 1
    if i == 1:
        j = 0

    if objeto == 1 or estado[0] != 0:
        posiciones[i][0], estados[i], start[i] = FI.rock(fila, estado, start[i], tiempo)
    if objeto == 2 or estado[1] != 0:
        mapas[i][fila], estados[i] = FI.beer(columna, mapa[fila], estado, tiempo)
    if objeto == 3:
        mapas[i][fila], estados[i] = FI.coin(columna, mapa[fila], estado)
    if objeto == 4 or estado[3] != 0:
        mapas[i][fila], estados[i] = FI.octopus(columna, mapa[fila], estado, tiempo)
    if len(estados) == 2:
        if objeto == 5 or estados[j][4] != 0:
            mapas[i][fila], estados[j] = FI.tirachinas(columna, mapa[fila], estados[j], tiempo)
    return mapas, posiciones, estados, start


if __name__ == "__main__":
    midict = {"conn": [], "pos": [[14, 5], [14, 5]], "start": [True, False]}
    salidaP, cambio = check(0, {"msg": "L"}, midict)
    print(salidaP)
    print("---------------------------")

    salidaS, cambio = check(0, {"go": ""}, midict)
    print(all(salidaS["start"]))

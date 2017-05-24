def fposicion(i, mensaje, data):
    """
    funcion que corre si el cliente envia mensaje tipo msg
    :param i: indice del cliente
    :param mensaje: mensaje del cliente
    :param data: datos completos de todos los clientes

    :type data: dict
    """
    position = data["pos"]
    start = data["start"]  # si el juego no esta corriendo, no cambia de posicion
    if all(start) and mensaje == "L" and position[i][1] > 0:  # si no esta en el borde izqierdo
        position[i][1] -= 1
        chng = True
    elif all(start) and mensaje == "R" and position[i][1] < 9:  # si no esta en el borde derecho
        position[i][1] += 1
        chng = True
    else:
        chng = False  # si no se produce ningun cambio, no manda nada a los clientes ni mira las interacciones
    return data, chng


def fstart(i, data):
    """
    funcion que corre si el cliente envia mensaje tipo go
    :param i: indice del cliente
    :param data: datos completos de todos los clientes
    :type data: dict    
    """
    start = data["start"]
    start[i] = True
    chng = False  # no produce cambios que afecten al mapa, a la posicion o los estados
    return data, chng


if __name__ == "__main__":
    midict = {"pos": [[14, 5], [14, 5]], "start": [True, False]}
    print(midict)

    salidaS, cambio = fstart(1, midict)
    print("fposicion:", salidaS, "change:", cambio)

    salidaP, cambio = fposicion(0, "R", midict)
    print("fposicion:", salidaP, "change:", cambio)


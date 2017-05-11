def fposicion(i, mensaje, data):
    """
    funcion que corre si el cliente envia mensaje tipo msg
    :param i:
    :param mensaje:
    :param data:

    :type data: dict
    :return:
    """
    position = data["pos"]
    start = data["start"]
    print(all(start))
    if all(start) and mensaje == "L" and position[i] > 0:
        position[i] -= 1
        chng = True
    elif all(start) and mensaje == "R" and position[i] < 9:
        position[i] += 1
        chng = True
    else:
        chng = False
    return data, chng


def fstart(i, data):
    """
    funcion que corre si el cliente envia mensaje tipo go
    :param i:
    :param data:
    :type data: dict    
    
    :return:
    """
    start = data["start"]
    start[i] = True
    chng = False
    print(start)  # todo borrar si funciona
    return data, chng


if __name__ == "__main__":
    midict = {"conn": [], "pos": [5, 5], "start": [False, False]}
    salidaP, cambio = fposicion(0, "L", midict)
    print(salidaP)
    print("---------------------------")

    salidaS, cambio = fstart(1, midict)
    print(all(salidaS["start"]))

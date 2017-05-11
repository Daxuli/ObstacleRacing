import FuncionesMensaje as FM


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

if __name__ == "__main__":
    midict = {"conn": [], "pos": [5, 5], "start": [False, False]}
    salidaP, cambio = check(0, {"msg": "L"}, midict)
    print(salidaP)
    print("---------------------------")

    salidaS, cambio = check(0, {"go": ""}, midict)
    print(all(salidaS["start"]))


"""
ws.py: WebSocket

Código correspondiente al servidor del juego en python
Utiliza Tornado, que contiene funcionalidades de websocket

Cumple 2 funciones: 1) escuchar y enviar a los clientes, 2) cargar cada 1000 ms el bucle de gameloop
"""
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json
import numpy as np
import TypeChecker as TC
import GameLoop as GL

settings = {
    'debug': True,
    'static_path': 'static'}


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):
    data = {"conn": [], "pos": [], "start": [], "map": [], "stat": []}
    connections = data["conn"]  # lista con las direcciones de cada cliente
    position = data["pos"]  # lista con las posiciones de cada cliente
    status = data["stat"]   # lista con los estados(borracho, numero de monedas, etc.) de cada cliente
    start = data["start"]   # lista de True/False de clientes. True = cliente está preparado

    def open(self):
        """
        Al conectarse un cliente, añade a @data todos los datos necesarios del nuevo cliente
        indica en consola nueva conexión
        """
        self.connections.append(self)
        self.position.append([14, 5])
        self.start.append(False)
        self.data["map"].append(np.zeros((20, 10), dtype=int))
        self.status.append([0, 0, 0, 0, 0])

        print('New connection was opened')

    def on_message(self, message):
        """
        Se ejecuta siempre que el cliente envíe un mensaje al servidor(L, R o start)
        """
        i = self.connections.index(self)  # índice del cliente. Usado para distinguir los datos de cada cliente
        json_string = u'%s' % message
        msg = json.loads(json_string)
        self.data, change = TC.check(i, msg, self.data)  # distingue el tipo de mensaje y modifica @data

        if change:  # True si @data ha sido modificado
            self.data["map"], self.position, self.status, self.start = TC.interaccion(i, self.data["map"],
                                                                                      self.position, self.status,
                                                                                      self.start, False)
            mapas = map(np.matrix.tolist, self.data["map"])  # convertimos cada matriz en una lista
            mapalista = []
            for elem in mapas:
                mapalista.append(elem)  # añadimos cada lista a una general:[[mapa1], [mapa2]]
            for elem in self.connections:  # enviamos a cada cliente el nuevo estado
                i = self.connections.index(elem)
                elem.write_message({"index": i,  # lo único que recibe cada cliente distinto
                                    "msg": self.position, "map": mapalista, "stat": self.status})

    def on_close(self):
        """
        Se ejecuta al cerrarse una página
        """
        print('connection closed\n')
        i = self.connections.index(self)
        for llave in self.data.keys():  # eliminamos en cada valor de @data el elemento del índice i
            del data[llave][i]


application = tornado.web.Application([(r'/', IndexHandler), (r'/ws', WSHandler)], **settings)
"""settings es necesario para que el cliente pueda acceder a los svg y al script de js"""

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    main_loop = tornado.ioloop.IOLoop.instance()
    # listener
    data = WSHandler.data
    sched = tornado.ioloop.PeriodicCallback(lambda: GL.gameloop(data), 1000, io_loop=main_loop)
    # bucle del juego principal
    sched.start()
    main_loop.start()


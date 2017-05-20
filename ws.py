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
    connections = data["conn"]
    position = data["pos"]
    status = data["stat"]
    start = data["start"]

    def open(self):
        self.connections.append(self)
        self.position.append([14, 5])
        self.start.append(False)
        self.data["map"].append(np.zeros((20, 10), dtype=int))
        self.status.append([0, 0, 0, 0, 0])

        print('New connection was opened')
        self.write_message("Conn!")

    def on_message(self, message):
        i = self.connections.index(self)
        json_string = u'%s' % message
        msg = json.loads(json_string)
        self.data, change = TC.check(i, msg, self.data)

        if change:
            self.data["map"], self.position, self.status, self. start= TC.interaccion(i, self.data["map"], self.position,
                                                                                      self.status, self.start, False)
            mapas = map(np.matrix.tolist, self.data["map"])  # convertimos cada matriz en una lista
            mapalista = []
            for elem in mapas:
                mapalista.append(elem)  # añadimos cada lista a una general:[[mapa1], [mapa2]]
            for elem in self.connections:
                i = self.connections.index(elem)
                elem.write_message({"index": str(i), "msg": self.position,
                                    "map": mapalista, "stat": self.status})

    def on_close(self):
        print('connection closed\n')
        self.connections.remove(self)


application = tornado.web.Application([(r'/', IndexHandler), (r'/ws', WSHandler)],**settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    main_loop = tornado.ioloop.IOLoop.instance()
    data = WSHandler.data
    sched = tornado.ioloop.PeriodicCallback(lambda: GL.gameloop(data), 1000, io_loop=main_loop)
    sched.start()
    main_loop.start()


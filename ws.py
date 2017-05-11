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
    data = {"conn": [], "pos": [], "start": [], "map": []}
    connections = data["conn"]
    position = data["pos"]

    def open(self):
        self.connections.append(self)
        self.position.append(5)
        self.data["start"].append(False)
        self.data["map"].append(np.zeros((20, 10), dtype=int))

        print('New connection was opened')
        self.write_message("Conn!")

    def on_message(self, message):
        i = self.connections.index(self)
        json_string = u'%s' % message
        msg = json.loads(json_string)
        self.data, change = TC.check(i, msg, self.data)

        if change:  # todo cambiar a enviar data completo a los clientes en cuanto pasemos de mostrar posicion
            print(self.position)
            print('received message: %s\n' % message)

            for elem in self.connections:
                i = self.connections.index(elem)
                elem.write_message({"index": str(i), "msg": str(self.position)})

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


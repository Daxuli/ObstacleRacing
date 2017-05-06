import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        #self.write("This is your response")
        #self.finish()
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    connections = []
    position = []

    def open(self):
        self.connections.append(self)
        print('New connection was opened')
        self.write_message("Conn!")
        self.position.append(5)

    def on_message(self, message):
        i = self.connections.index(self)
        #print(type(message))
        json_string = u'%s' % (message)
        #print(json_string)
        msg = json.loads(json_string)
        #print(type(msg))
        message = msg['msg']
        if (message == "L" and self.position[i] > 0):
            self.position[i] -= 1
            change = True
        elif (message == "R" and self.position[i] < 10):
            self.position[i] += 1
            change = True
        else:
            change = False

        if change:
            print(self.position)
            print('received message: %s\n' %message)

            nplayers = len(self.connections)
            for elem in self.connections:
                i = self.connections.index(elem)
                elem.write_message({"msg": "You: " + str(self.position[i])}, binary=False)
                for j in range(nplayers):
                    if j == i:
                        continue
                    elem.write_message({"msg": "Player %s:" % j + str(self.position[j])})



    def on_close(self):
        print('connection closed\n')
        self.connections.remove(self)


application = tornado.web.Application([(r'/', IndexHandler),(r'/ws', WSHandler),])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
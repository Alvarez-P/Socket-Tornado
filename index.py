import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import time, os, json

try:
    g_clients  = []

    class WebWSHandler(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
            return True

        def open(self):
            # self.callback = PeriodicCallback(self.send_temp, 120)
            # self.callback.start()
            if self not in g_clients:
                print('Append connection')
                g_clients.append(self)
            print (f'\nWebsocket Connect: {self}')
            print('Client number: ' + str(len(g_clients)))
        
        def on_message(self, message):
            self.send_message_to_all(self, message)

        def on_close(self):
            if self in g_clients:
                print ('Websocket closed: ' + str(self))
                g_clients.remove(self)
            print('>>> Disconnect <<<')

        def send_message_to_all(self, message):
            for c in g_clients:
                if(c != self):
                    named_tuple = time.localtime()
                    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
                    c.write_message(json.dumps(message))

    WebApp = tornado.web.Application([
        (r'/', WebWSHandler),
    ])
    
    if __name__ == "__main__":
        http_server = tornado.httpserver.HTTPServer(WebApp)
        http_server.listen(5000)
        http_server.start(num_processes = 1)
        myIP = socket.gethostbyname(socket.gethostname())
        print (f'*** Websocket Server Started at {myIP} ***')

        tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    print('\nSaliendo...')
    os._exit(0)

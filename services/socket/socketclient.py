import time
import simplejson as json
from threading import Thread

from socketIO_client import SocketIO, BaseNamespace


class SocketClient(object):
    sock = None
    callbacks = dict()

    def __init__(self, hostname, port):
        self.sock = SocketIO(hostname, port, wait_for_connection=False)
        self.__worker = Thread(target=self.__worker, args=())
        self.__worker.setDaemon(True)
        self.__worker.start()

    def on(self, event, callback):
        self.sock.on(event, callback)

    def emit(self, event, data):
        self.sock.emit(event, data)

    def wait(self, seconds):
        if self.sock.connected:
            self.sock.wait(seconds=seconds)

    def __worker(self):
        self.sock.wait()


def on_config_update(data):
    for key in data.keys():
        print "Config {0}={1}".format(key.upper(), data[key])


def on_registered(data):
    print("registered {0}".format(data))


class SocketDelegate(object):

    def on_cfg_update(self, data):
        print "on_cfg_update"
        for key in data.keys():
            print "Config {0}={1}".format(key.upper(), data[key])


if __name__ == '__main__':
    rtSock = SocketClient('admin.self-o-matic.com', 80)
    rtSock.emit('register', '12344')
    delegate = SocketDelegate()

    rtSock.on('config_update', delegate.on_cfg_update)

    while True:
        rtSock.wait(seconds=0.4)

    # rtSock.wait()

# coding=utf-8

# Progetto: Selfie-O-Matic
# Scope   : Client for PubPub cloud service

from threading import Thread
from pubnub import PubnubTornado as Pubnub


class PubNubClient(object):
    channel = ''

    def __init__(self, serial, publish_key, subscribe_key):
        self.pubnub = Pubnub(publish_key=publish_key,
                             subscribe_key=subscribe_key)
        self.channel = 'ch-{0}'.format(serial)
        self.__worker = Thread(target=self.__worker, args=())
        self.__worker.setDaemon(True)
        self.__worker.start()

    def on(self, event, callback):

        self.pubnub.subscribe(self.channel,
                              callback=self.__makeCallback(event, callback), error=self.__error_cb,
                              connect=self.__connect_cb,
                              reconnect=self.__reconnect_cb, disconnect=self.__disconnect_cb)

    def emit(self, event, data):
        payload = {'event': event, 'data': data}
        self.pubnub.publish(channel=self.channel, message=payload)

    def __worker(self):
        self.pubnub.start()

    def __makeCallback(self, event, callback):
        def subscribe_cb(message, channel):
            if 'event' in message and message['event'] == event:
                callback(message)
        return subscribe_cb

    def __connect_cb(self, message):
        print "connect message {0}".format(message)

    def __reconnect_cb(self, message):
        print "reconnect message {0}".format(message)

    def __disconnect_cb(self, message):
        print "disconnect message {0}".format(message)

    def __error_cb(self, message):
        print "error message {0}".format(message)


def on_registered(data):
    print("registered {0}".format(data))

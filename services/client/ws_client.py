import requests
import json
from posixpath import join as urljoin


class WsClient(object):

    def __init__(self, base_url):
        self.__base_url = base_url

    def register_myself(self, serial, name):
        service_url = urljoin(self.__base_url, "api/machines/")
        data = json.dumps({u"serial": serial, u"name": name})
        r = requests.post(url=service_url,
                          data=data,
                          headers={'content-type': 'application/json'}
                          )

        return (r.status_code >= 200 and r.status_code < 300) or r.status_code == 304

    def get_config(self, serial):
        res = None
        service_url = urljoin(
            self.__base_url, "api/machines/", serial, "config")
        r = requests.get(url=service_url)

        if r.status_code == 200:
            res = r.json()

        return res

    def store_config(self, serial, config):
        pass

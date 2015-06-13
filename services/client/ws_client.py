import requests, json
from posixpath import join as urljoin

BASE_URL = "http://api.self-o-matic.com/api/machines/"


class WsClient(object):

	def register_myself(self, serial):
		service_url = urljoin(BASE_URL, "machine_serials")
		data = json.dumps({'serial': serial}) 
		r = requests.post(service_url, data)
		return r.json

	def get_config(self):
		pass


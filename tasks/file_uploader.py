# coding=utf-8

# Progetto	: Self-O-Matic
# Note		: Upload multipart/form-data file utility

import os
import requests
import logging

class UploaderHelper(object):
    post_url = ''

    def __init__(self, url):
        self.post_url = url

    def upload_file(self, path,  filepath):
        filename = os.path.basename(filepath)
        file = {filename: open(filepath, 'rb')}

        response = requests.post(self.post_url + path, files=file)
        logging.debug("-- UPLOAD RESPONSE {0}".format(response.status_code))
        return response.status_code == 200

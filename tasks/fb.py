import facebook


class FacebookHelper(object):
    _app_id = None
    _access_token = None

    def __init__(self, app_id, access_token):
        self._app_id = app_id
        self._access_token = access_token

    def get_object_info(self, object_id):
        cfg = {
            "page_id": self._app_id,
            "access_token": self._access_token
        }

        api = facebook.GraphAPI(access_token=cfg['access_token'])
        return api.get_object(id=object_id)

    def post_image(self, image_path):
        cfg = {
            "page_id": self._app_id,
            "access_token": self._access_token
        }

        api = self.__get_api(cfg)
        status = api.put_photo(image=open(image_path), message='')

        return status

    def post_on_album(self, image_path, album_id):
        if type(album_id) != str:
            raise TypeError("album_id must be a string")

        cfg = {
            "page_id": self._app_id,
            "access_token": self._access_token
        }

        api = facebook.GraphAPI(access_token=cfg['access_token'])

        print("POSTING ON FB  album:{0} file:{1}".format(album_id, image_path))

        status = api.put_photo(image=open(image_path), album_id=album_id)

        return status

    def __get_api(self, cfg):
        graph = facebook.GraphAPI(access_token=cfg['access_token'])

        # Get page token to post as the page. You can skip
        # the following if you want to post as yourself.
        # resp = graph.get_object('me/accounts')
        resp = graph.get_object(self._app_id)

        print("RESP " + str(resp))
        page_access_token = None

        for page in resp['data']:
            if page['id'] == cfg['page_id']:
                page_access_token = page['access_token']
                print("page access token {0} ({1})".format(
                    page_access_token, page))

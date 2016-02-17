import facebook
import settings


def post_image(image_path):
    cfg = {
        "page_id": settings.FB_APP_ID,
        "access_token": settings.FB_ACCESS_TOKEN
    }

    api = __get_api(cfg)
    status = api.put_photo(image=open(image_path), message='')

    return status


def post_on_album(image_path, album_id, message):
    api = __get_api()
    status = api.put_photo(image=open(image_path),
                           album_id=album_id, message=message)

    return status


def post_page_cover(page_id, image_path):
    api = __get_api()
    # TODO: Check se la foto viene uploadata nella pagina
    status = api.put_photo(image=open(image_path))

    if 'id' in status:
        post_url = '/v2.5/{0}?cover={1}&access_token={2}'.format(page_id, status['id'], settings.FB_ACCESS_TOKEN)
        print post_url
        api.request(post_url, post_args={})


def __get_api():
    cfg = {
        "page_id": settings.FB_APP_ID,
        "access_token": settings.FB_ACCESS_TOKEN
    }

    return facebook.GraphAPI(access_token=cfg['access_token'])

from twython import Twython
import settings


class TwitterHelper(object):
    _twitter = None

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):

        _twitter = Twython(consumer_key,
                           consumer_secret,
                           access_token,
                           access_token_secret)

    def tweet_image(self, image_path, status_message):

        photo = open(image_path, 'rb')
        response = twitter.upload_media(media=photo)

        return _twitter.update_status(status=status_message,
                                      media_ids=[response['media_id']])

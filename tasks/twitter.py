from twython import Twython
import settings


def tweet_image(image_path, status_message):
    twitter = Twython(settings.TW_CONSUMER_KEY,
                      settings.TW_CONSUMER_SECRET,
                      settings.TW_ACCESS_TOKEN,
                      settings.TW_TW_ACCESS_TOKEN_SECRET)

    photo = open(image_path, 'rb')
    response = twitter.upload_media(media=photo)

    return twitter.update_status(status=status_message,
                                 media_ids=[response['media_id']])

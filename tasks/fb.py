import os

import facebook
import settings

def main():
  # Fill in the values noted in previous steps here
  status = post_on_album("/Users/fabrizio/Downloads/selfimachine.jpg", settings.FB_ALBUM_ID)
  if 'post_id' in status:
    print "POST AVVENUTO"
    
  print "Status res {0}".format(status)
 
def post_image(image_path):
  cfg = {
    "page_id"      : settings.FB_APP_ID,  
    "access_token" : settings.FB_ACCESS_TOKEN   
  }

  api = get_api(cfg)
  status = api.put_photo(image=open(image_path), message='')

  return status

def post_on_album(image_path, album_id):
  
  cfg = {
    "page_id"      : settings.FB_APP_ID,  
    "access_token" : settings.FB_ACCESS_TOKEN   
  }

  api = facebook.GraphAPI(access_token=cfg['access_token'])
  status = api.put_photo(image=open(image_path), album_id=album_id)
 
  return status

def get_api(cfg):
  graph = facebook.GraphAPI(access_token=cfg['access_token'])

  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  #resp = graph.get_object('me/accounts')
  resp = graph.get_object(settings.FB_APP_ID)

  print "RESP " + str(resp)
  page_access_token = None

  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
      print "page access token {0} ({1})".format(page_access_token, page)

  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()
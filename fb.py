import facebook
import settings

def main():
  # Fill in the values noted in previous steps here
  cfg = {
    "page_id"      : settings.FB_APP_ID,  
    "access_token" : settings.FB_ACCESS_TOKEN   
    }

  api = get_api(cfg)
  msg = "This is a test"
  status = api.put_wall_post(msg)

 
def post_image(image_path):
   cfg = {
      "page_id"      : settings.FB_APP_ID,  
      "access_token" : settings.FB_ACCESS_TOKEN   
   }

   api = get_api(cfg)
   status = api.put_photo(image=open(image_path), message='')
   return status


def get_api(cfg):
  graph = facebook.GraphAPI(access_token=cfg['access_token'])

  # Get page token to post as the page. You can skip 
  # the following if you want to post as yourself. 
  resp = graph.get_object('me/accounts')

  page_access_token = None

  for page in resp['data']:
    if page['name'] == 'Petaboo':
      page_access_token = page['access_token']

  graph = facebook.GraphAPI(page_access_token)
  return graph
  # You can also skip the above if you get a page token:
  # http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
  # and make that long-lived token as in Step 3

if __name__ == "__main__":
  main()
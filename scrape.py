import re
import requests
import time
import tweepy

BEARER_TOKEN = ''
USER_AGENT = ''

auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
api = tweepy.API(auth)

s = requests.Session()
s.headers['User-Agent'] = USER_AGENT

categories = [' ', 'art', 'nft', 'dao', '$']
user_ids = set()

with open('user-data.txt', 'w') as file:
  for category in categories:
    for i in range(50):
      users = api.search_users(q=f'.eth {category}', page=i)

      for user in users:
        parse = re.search(r'[a-zA-Z0-9_]+\.eth', user.name + ' ' + user.description)
        if parse is None or user.id_str in user_ids:
          continue
        user_ids.add(user.id_str)

        address = parse.group()
        file.writelines([line+'\n' for line in [category, user.id_str, user.name, str(user.followers_count), str(user.friends_count)]])

        resp = s.get(f'https://etherscan.io/enslookup-search?search={address}')
        if 'is not currently registered' in resp.text:
          file.write('INVALID\n\n')
        else:
          file.write('VALID\n\n')

        time.sleep(6)
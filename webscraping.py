# import requests
# from bs4 import BeautifulSoup

# url = "https://www.trackalytics.com/the-most-followed-twitter-profiles/page/1/"

# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')

# table = soup.find('table', class_ = 'table table-bordered table-striped')
# name = []
# follower = []

# # for team in table.find_all('tbody'):
# rows = table.tbody.find_all('tr')
# for row in rows:
#   temp = 0
#   for td in row.find_all('td'):
#     if temp == 1:
#       name.append(td.text.replace('\n', ' ').strip())
#     elif temp == 2:
#       f = td.text.replace('\n', ' ').strip().split('(')[0]
#       follower.append(f)
#       # follower.append(td.text.replace('\n', ' ').strip())
#     temp += 1


# print(name)


from bs4 import BeautifulSoup
import requests
import re

name = []
follower = []
url_twitter_follower = 'https://www.trackalytics.com/the-most-followed-twitter-profiles/page/{page_id}/'
for page_id in range(1, 2):
  url = url_twitter_follower.format(page_id=page_id)
  try:
    r = requests.get(url)
  except:
    continue

  soup = BeautifulSoup(r.text, 'html.parser')

  table = soup.find('table', class_ = 'table table-bordered table-striped')
  

  # for team in table.find_all('tbody'):
  rows = table.tbody.find_all('tr')
  for row in rows:
    temp = 0
    for td in row.find_all('td'):
      if temp == 1:
        for href in td.find_all('a'):
          link = href['href']
          name = link.split('/')[-2]
          print(name)
      #   name.append(td.text.replace('\n', ' ').strip())
      elif temp == 2:
        f = td.text.replace('\n', ' ').strip().split('(')[0]
        f = int(f.replace(',', ''))
        follower.append(f)
        # follower.append(td.text.replace('\n', ' ').strip())
      temp += 1

print(follower)
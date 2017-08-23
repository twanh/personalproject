import requests
from bs4 import BeautifulSoup
import json

# GTA TEST

query = 'gta'
url = 'https://g2a.com/lucene/search/filter?jsoncallback=&skip=&minPrice=0.00&maxPrice=1422.00&cc=NL&stock=all&event=&search={}&genre=0&cat=0&sortOrder=popularity+desc&start=0&rows=12&steam_app_id=&steam_category=&steam_prod_type=&includeOutOfStock=false&includeFreeGames=false&isWholesale=false&_=1503469082372'.format(query)

req = requests.get(url)

print('Status Code: {}'.format(req.status_code))
print('-' * 50, end='\n')
# print(req.text)

# Remove weird ()
data = req.text[1:-1]

json_data = json.loads(data)

# with open('testfile.json', 'w') as f:
#     f.write(json.dumps(json_data))


num_found = json_data['numFound']
print(num_found)
print('-' * 50, end='\n')

docs = json_data['docs']

results = []

for doc in docs:
    game_name = doc['name']
    price = doc['minPrice']
    slug = doc['slug']
    small_img = doc['smallImage']

    print('Name: {}'.format(game_name))
    print('Price: {}'.format(price))
    print('Slug: {}'.format(slug))
    print('Img: {}'.format(small_img))
    print('-' * 50, end='\n')

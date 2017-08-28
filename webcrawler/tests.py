import crawlers
import json

# Testing
def test_g2a_search():
    ''' Test the search crawling of the G2a webcrawler '''
    g3a = crawlers.G2a()
    s = g3a.search('gta')
    print('-'*10, end='\n')
    print('Type: {}'.format(type(s)))
    print('-'*10, end='\n')
    print('List: ', end='\n')
    print(str(s))
    print('-'*10, end='\n')
    for game in s:
        print(game['name'])
        print(game['price'])
        print(game['url'])
        print('-'*10)

def test_g2a_game():
    ''' Test the game crawling of the G2a webcrawler '''
    url = 'https://www.g2a.com/grand-theft-auto-v-rockstar-key-global-i10000000788017'
    g2a = crawlers.G2a()
    game_info = g2a.game(url)
    print('-'*10)
    print('Type: {}'.format(type(game_info)))
    print('-'*10, end='\n')
    print('Dict: ', end='\n')
    print(str(game_info))
    print('-'*10, end='\n')
    print('Name: {}'.format(game_info['name']))
    print('Desc: {}'.format(game_info['desc']))
    print('Desc Text: {}'.format(game_info['desc_text']))
    print('Img URL: {}'.format(game_info['img']))
    print('Slider Images URLs: {}'.format(game_info['slider_img']))
    print('Price: {}'.format(game_info['price']))
    print('-'*10)

def kinguin_search():
    ''' Test the search crawling of the kinguin webcrawler '''
    url = 'https://www.kinguin.net/catalogsearch/result/index/?p=1&q={}&order=bestseller&dir=desc&max_price=143&dir_metacritic=desc&hide_outstock=1'
    query = 'grand theft auto'
    king = crawlers.Kinguin(url)
    search = king.search(query)
    s =  json.dumps(search)
    print(s)

def kinguin_game():
    search_url = 'https://www.kinguin.net/catalogsearch/result/index/?p=1&q={}&order=bestseller&dir=desc&max_price=143&dir_metacritic=desc&hide_outstock=1'
    url = 'https://www.kinguin.net/category/15836/grand-theft-auto-v-rockstar-digital-download-key/'
    king = crawlers.Kinguin(search_url)
    game = king.game(url)
    print(game)

kinguin_game()
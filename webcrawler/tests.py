from webcrawler.crawlers import *
import json

# Testing
def test_g2a_search():
    ''' Test the search crawling of the G2a webcrawler '''
    g3a = G2a()
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
    g2a = G2a()
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
    king = Kinguin(url)
    search = king.search(query)
    s =  json.dumps(search)
    print(s)

def kinguin_game():
    search_url = 'https://www.kinguin.net/catalogsearch/result/index/?p=1&q={}&order=bestseller&dir=desc&max_price=143&dir_metacritic=desc&hide_outstock=1'
    url = 'https://www.kinguin.net/category/15836/grand-theft-auto-v-rockstar-digital-download-key/'
    king = Kinguin(search_url)
    game = king.game(url)
    print(game)

def gamestop_game():
    search_url = ''
    url = 'http://www.gamestop.com/pc/games/grand-theft-auto-v/115461'
    gamestop = Gamestop(search_url)
    game = gamestop.game(url)
    print(game)

def gamestop_search():
    search_url = 'http://www.gamestop.com/browse/pc?nav=16k-3-{},28-wa2,138c'
    gamestop = Gamestop(search_url)
    results = gamestop.search('grand theft auto v')
    print(results)

def gameranking_rating():
    search_url = 'http://www.gamerankings.com/browse.html?search={}&numrev=3&site=pc'
    ganeranking = GameRanking(search_url)
    rating = ganeranking.rating('http://www.gamerankings.com/pc/805606-grand-theft-auto-v/index.html')
    print(rating)

def gameranking_search():
    search_url = 'http://www.gamerankings.com/browse.html?search={}&numrev=3&site=pc'
    ganeranking = GameRanking(search_url)
    rating = ganeranking.search_rating('grand theft auto v')
    print(rating)
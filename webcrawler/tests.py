from webcrawler.crawlers import G2a, Kinguin, Gamestop, Gameraking, Reddit


def test_g2a_all():
    game = G2a.game('https://www.g2a.com/grand-theft-auto-v-rockstar-key-global-i10000000788017')
    search = G2a.search(query='grand theft auto')
    
    print('G2a')
    print('-'*50)
    print('Game:')
    print(game)
    print('-'*50)
    print('Search: ')
    print(search)


def test_kinguin_all():
    game = Kinguin.game('https://www.kinguin.net/category/15836/grand-theft-auto-v-rockstar-digital-download-key/')
    search = Kinguin.search('grand theft auto')
    print(game)
    print('-'*50)
    print('\n\n')
    print(search)

def test_gamestop_all():
    game = Gamestop.game('http://www.gamestop.com/pc/games/grand-theft-auto-v/115461')
    search = Gamestop.search('grand theft auto')
    print(game)
    print('-'*50)
    print('\n\n')
    print(search)
    
def test_gameranking():
    game = Gameraking.game_rating('http://www.gamerankings.com/pc/805606-grand-theft-auto-v/index.html')
    search = Gameraking.search_rating('grand theft auto')
    print(game)
    print('-'*50)
    print('\n\n')
    print(search)
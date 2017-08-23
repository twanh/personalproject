import crawlers

# Testing
def test_g2a_search():
    '''
    Test the search crawling of the G2a webcrawler 
    '''
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
        
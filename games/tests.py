from games.models import GameManager

# Simply Test GameManager
def test_gamemanager():
    gm = GameManager()
    name = 'Grand Theft Auto V'
    urls = {'g2a':'https://www.g2a.com/grand-theft-auto-v-rockstar-key-global-i10000000788017',
            'kinguin': 'https://www.kinguin.net/category/15836/grand-theft-auto-v-rockstar-digital-download-key/'}
    
    created = gm._create_from_crawl(name, urls)

if __name__ == '__main__':
    test_gamemanager()

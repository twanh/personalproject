import decimal

from django.db import models

from webcrawler.crawlers import G2a, Kinguin, CrawlRequestError, CrawlDataError

# from sellers.models import Sellers 

class GameManager(models.Manager):

    def _create_from_crawl(self, name=None, urls={}):
        '''
        Create a game model by crawling the sites

        Args:
            name (str): The name of the game - if not supplied the one listed on g2a will be used
            urls (dict): Dictionary containing the urls to the game pages 
                'g2a': url
                'kinguin': url
                'greenman': url
                'gamestop': url

        Return:
            Model
        '''
        # TODO: Once selles are made
        # G2a_crawler = G2a(Seller.search_url)
        # For now
        G2A_DEFAULT_SEARCH_URL = 'https://g2a.com/lucene/search/filter?jsoncallback=&skip=&minPrice=0.00&maxPrice=1422.00&cc=NL&stock=all&event=&search={}&genre=0&cat=0&sortOrder=popularity+desc&start=0&rows=12&steam_app_id=&steam_category=&steam_prod_type=&includeOutOfStock=false&includeFreeGames=false&isWholesale=false&_=1503469082372'
        g2a_crawler = G2a(G2A_DEFAULT_SEARCH_URL)
        KINGUIN_DEFAULT_SEARCH_URL = 'https://www.kinguin.net/catalogsearch/result/index/?p=1&q={}&order=bestseller&dir=desc&max_price=143&dir_metacritic=desc&hide_outstock=1'
        kinguin_crawler = Kinguin(KINGUIN_DEFAULT_SEARCH_URL)

        # VARIABLES THAT WILL BE INPUTTED TO THE MODEL OBJ
        game_name        = name
        game_desc        = None
        img_url          = None
        original_price   = None
        g2a_price        = None
        kinguin_price    = None
        greenman_price   = None
        gamestop_price   = None
        g2a_url          = None
        kinguin_url      = None
        greenman_url     = None
        gamestop_url     = None
        images           = []

        if 'g2a' in urls:
            try:
                gta_results = g2a_crawler.game(urls['g2a'])
                
                # Check if the game name existst
                if not game_name:
                    game_name = gta_results['name']
                if not game_desc:
                    game_desc = gta_results['desc']
                if not img_url:
                    img_url = gta_results['img']
                
                g2a_url = urls['g2a']
                g2a_price = gta_results['price']
                for img in gta_results['slider_img']:
                    images.append(img)
                
            except CrawlRequestError:
                pass
            except CrawlDataError:
                pass
    
        if 'kinguin' in urls:
            try:
                kinguin_results = kinguin_crawler.game(urls['kinguin'])

                # Check if the game name exists
                if not game_name:
                    game_name = kinguin_results['name']
                if not game_desc:
                    game_desc = kinguin_results['desc']
                if not img_url:
                    img_url = kinguin_results['img_url']
                
                kinguin_url = urls['kinguin']
                kinguin_price = kinguin_results['price']

            except CrawlRequestError:
                pass
        
        # TODO: Implement greenhouse, gamestop
        # TODO: REMOVE 'x_price'
        new_game = Game(name = game_name,
                       desc = game_desc,
                       image_url = img_url,
                       original_price = '0',
                       g2a_price = g2a_price,
                       g2a_url = g2a_url,
                       kinguin_price = kinguin_price,
                       kinguin_url = kinguin_url,
                       greenman_price = 'greenman_price',
                       greenman_url = greenman_url,
                       gamestop_price = 'gamestop_price',
                       gamestop_url = gamestop_url,
                       images = images
                       )
        new_game.save()

        return new_game
            

class Game(models.Model):
    ''' The Model to store games '''

    # Name of the game
    name = models.CharField(max_length=100,
                            blank=True)

    # Description of the game
    desc = models.TextField(blank=True)

    image_url = models.URLField(verbose_name='Image URL',
                                null=True,
                                blank=True)
    
    # Original Price of the game
    original_price = models.CharField(max_length=15,
                            blank=True)

    # Price on g2a
    g2a_price = models.CharField(max_length=15,
                            blank=True)

    # Url on g2a
    g2a_url = models.URLField(verbose_name='G2a URL',
                              null=True,
                              blank=True
                             )

    # Price on kinguin
    kinguin_price = models.CharField(max_length=15,
                            blank=True)

    kinguin_url = models.URLField(verbose_name='Kinguin URL',
                              null=True,
                              blank=True
                             )

    # Price on greenman
    greenman_price = models.CharField(max_length=15,
                            blank=True)

    greenman_url = models.URLField(verbose_name='Greenman URL',
                              null=True,
                              blank=True
                             )                            

    # Price on gamestop
    gamestop_price = models.CharField(max_length=15,
                            blank=True)

    gamestop_url = models.URLField(verbose_name='Gamestop URL',
                              null=True,
                              blank=True
                             )
                
    # Image ulrs to images for the game
    images = models.TextField(blank=True, default='[]')


    def __str__(self):
        return self.name 

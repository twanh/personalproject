import decimal
from django.db import models
import json
from webcrawler import crawlers

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
                'gameranking': url
                

        Return:
            Model
        '''

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
        rating           = None
        reddit           = None   
        images           = []

        if 'g2a' in urls:
            if urls['g2a'] != '':
                g2a_game = crawlers.G2a.game(urls['g2a'])
                if not game_name:
                    game_name = g2a_game['name']
                if not game_desc:
                    game_desc = g2a_game['desc']
                if not img_url:
                    img_url = g2a_game['img']
                
                g2a_price = g2a_game['price']
                g2a_url = urls['g2a']

                for img in g2a_game['slider_img']:
                    images.append(img)

        if 'kinguin' in urls:
            if urls['kinguin'] != '':
                kinguin_game = crawlers.Kinguin.game(urls['kinguin'])
                if not game_name:
                    game_name = kinguin_game['name']
                if not game_desc:
                    game_desc = kinguin_game['desc']
                if not img_url:
                    img_url = kinguin_game['img_url']
                
                kinguin_price = kinguin_game['price']
                kinguin_url = urls['kinguin']

        if 'gamestop' in urls:
            if urls['gamestop'] != '':
                gamestop_game = crawlers.Gamestop.game(urls['gamestop'])
                if not game_name:
                    game_name = gamestop_game['name']
                if not game_desc:
                    game_desc = game_desc['desc']
                
                gamestop_price = gamestop_game['price']
                gamestop_url = urls['gamestop']        

        if 'gameranking' in urls:
            if urls['gameranking'] != '':
                rating = int(crawlers.Gameraking.game_rating(urls['gameranking']))
        else:
            rating = crawlers.Gameraking.search_rating(game_name)
            if len(rating) >= 2:
                if rating[1]:
                    rating = decimal.Decimal(rating[1])
                else:
                    rating = None
            else:
                rating = None

        try:
            reddit = crawlers.Reddit.get_community_url(game_name)
        except crawlers.CrawlRequestError:
            # Initiate a timer to do this later,
            # Look trough db and see al reddit nones?
            reddit = None

        images = json.dumps(images)

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
                        gamestop_price = gamestop_price,
                        gamestop_url = gamestop_url,
                        images = images,
                        rating = rating,
                        community_reddit = reddit
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
                            blank=True,
                            null=True)

    # Url on g2a
    g2a_url = models.URLField(verbose_name='G2a URL',
                              null=True,
                              blank=True
                             )

    # Price on kinguin
    kinguin_price = models.CharField(max_length=15,
                            blank=True,
                            null=True)

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
                            blank=True,
                            null=True)

    gamestop_url = models.URLField(verbose_name='Gamestop URL',
                              null=True,
                              blank=True
                             )
                
    # Image ulrs to images for the game
    images = models.TextField(blank=True, default='[]')
    
    # Rating for the game
    rating = models.IntegerField(blank=True, null=True)

    # Reddit community url
    community_reddit = models.URLField(verbose_name='Reddit community urls',
                                    blank=True,
                                    null=True) 
    def __str__(self):
        return self.name 

    
    def return_images_dict(self):
        imgs = self.images
        img_dict = json.loads(imgs)
        return img_dict

    def get_best_price(self):
        prices = [self.g2a_price, self.kinguin_price, self.greenman_price, self.gamestop_price]
        rev_prices = []
        for price in prices:
            print('Price!', price)
            if price is not None:
                if len(str(price)) > 0:
                    try:
                        a = int(price[0])
                        rev_prices.append(price)
                    except ValueError:
                        pass
        return min(rev_prices)

    
    def get_best_seller(self):
        prices = [self.g2a_price, self.kinguin_price, self.greenman_price, self.gamestop_price]
        rev_prices = []
        for price in prices:
            print('Price!', price)
            if price is not None:
                if len(str(price)) > 0:
                    try:
                        a = int(price[0])
                        rev_prices.append(price)
                    except ValueError:
                        pass
        best_price = min(rev_prices)    
        index = rev_prices.index(best_price)
        print('index' + str(index))
        return (index + 1)

    def get_rating(self):
        ''' Get the rating out of 10 instead of 100 '''
        return str(self.rating/10)[:3]

    def get_kinguin_ref_url(self):
        ''' Get the url for the game on kinguin with the refferal code attached '''
        return ''.join([self.kinguin_url, '?r=42864'])
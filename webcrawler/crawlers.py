import json
from json.decoder import JSONDecodeError

import requests

from bs4 import BeautifulSoup as BS

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# CONSTANT VARIABLES
# Search urls, can be used as reference or default when the sellers model is not functional

G2A_DEFAULT_SEARCH_URL = 'https://g2a.com/lucene/search/filter?jsoncallback=&skip=&minPrice=0.00&maxPrice=1422.00&cc=NL&stock=all&event=&search={}&genre=0&cat=0&sortOrder=popularity+desc&start=0&rows=12&steam_app_id=&steam_category=&steam_prod_type=&includeOutOfStock=false&includeFreeGames=false&isWholesale=false&_=1503469082372'

KINGUIN_DEFAULT_SEARCH_URL = 'https://www.kinguin.net/catalogsearch/result/index/?p=1&q={}&order=bestseller&dir=desc&max_price=143&dir_metacritic=desc&hide_outstock=1'

GAMESTOP_DEFAULT_SEARCH_URL = 'http://www.gamestop.com/browse/pc?nav=16k-3-{},28-wa2,138c'

GAMERANKING_DEFAULT_SEARCH_URL = 'http://www.gamerankings.com/browse.html?search={}&numrev=3&site=pc'

REDDIT_SEARCH_URL = 'https://www.reddit.com/search?q={}'

# EXCEPTIONS
# Used in the crawlers to make sure that if something goes wrong we
# have a corresponding exception

class CrawlRequestError(Exception):
    ''' 
    Raise when something goes wrong while crawling a page
    specificly when the request goes wrong. 
    '''
    pass

class CrawlUrlError(Exception):
    " Raise when the url is wrong "
    pass


class CrawlNoResultsError(Exception):
    " Raise when there are nor results when crawling "
    pass

class CrawlDataError(Exception):
    " Raise when the data type is not matched "
    pass

# HELPER FUNCTIONS
# Help with the crawlers

def validate_url(url):
    '''
    Use to validate url
    Args:
        url (str): The url to validate
    Returns:
        (boolean): True if url validation was success
    Raises:
        CrawlUrlError: When the url was not valid
    '''

    validator = URLValidator()
    try:
        validator(url)
        return True

    except ValidationError:
        raise CrawlUrlError('Url validion failed for url: {}'.format(url))

    return False
    

# Crawler Classes
# The classes that will actualy crawl the sites.


class G2a:
    ''''''

    @staticmethod
    def game(self, url):
        ''''''
        pass

    @staticmethod
    def search(self, query, url=G2A_DEFAULT_SEARCH_URL):
        ''''''
        pass


class Kinguin:
    '''''''

    @staticmethod
    def game(self, url):
        ''''''
        pass

    @staticmethod
    def search(self, query, url=KINGUIN_DEFAULT_SEARCH_URL):
        ''''''
        pass


class Gamestop:
    ''''''

    @staticmethod
    def game(self, url):
        '''''''
        pass

    @staticmethod
    def search(self, query, url=GAMESTOP_DEFAULT_SEARCH_URL):
        '''''''
        pass


class Gameraking:
    ''''''

    @staticmethod
    def game_rating(self, url):
        ''''''
        pass
    
    @staticmethod
    def search_rating(self, query, url=GAMERANKING_DEFAULT_SEARCH_URL):
        ''''''
        pass


class Reddit:
    ''''''

    @staticmethod
    def get_community_link(self, query, url=REDDIT_SEARCH_URL):
        ''''''
        pass
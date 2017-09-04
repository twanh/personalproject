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
    
def get_html(url):
    '''
    Request url and return the pages html
    Args:
        url (str): The url to request
    Returns:
        html (str): The content of the url/page
    Raises:
        CrawlRequestError: When the request failed 
    '''
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        return r.text
    else:
        raise CrawlRequestError('Request to url: {}, failed with code {}'.format(url, r.status_code))

    return None


# Crawler Classes
# The classes that will actualy crawl the sites.


class G2a:
    ''' Webcrawler for G2a.com '''

    @staticmethod
    def game(self, url):
        '''
        Crawl the game's page
        and extract all the relevant information from the page.
        Args:
            url (str): The url to the game's page
        Returns:
            (dict) Results - The relevant information:
                'name'      : 'The games name'
                'desc'      : 'The games description'
                'desc_raw'  : 'Raw text from the description'
                'img'       : 'The main image for the game, url'
                'slider_img': [The urls for images from the game]
                'price'     : 'The game's price'
        Raises:
            CrawlUrlError: If the url is invalid
            CrawlRequestError: If the request failed
        '''
        
        # Url validation
        # We do this to ensure the url is valid
        # We do not use the return because
        # if the validation failed we already raised an exception
        # and a True boolean is not of use.
        validate_url(url)

        # Declare all the return variables
        # We do this because we do not want
        # to return a not declared variable.
        # This way we will always return something
        # even if it does not exist - None
        name        = None
        price       = None
        desc        = None
        raw_desc    = None
        img         = None
        slider_img  = None

        # Request the url and create the BeautifullSoup Obj
        soup = BS(get_html(url))

        # Get the name of the game
        # - Find class nameContent
        # - Check if nameContent is bigger than or equal to 1 (it has results in it)
        #   - Find the h1 in the first ([0]) result
        #   - Check if it exists (is not None)
        #       - Get the text (already stripped)
        game_name = soup.find_all(class_='nameContent')
        if len(game_name) >= 1:
            game_name = game_name[0].find('h1')
            if game_name:
                game_name = game_name.get_text(strip=True)
            else:
                print('[CRAWLER > G2a > game > name]: h1 was not found in game_name[0]')                
                game_name = None
                
        else:
            print('[CRAWLER > G2a > game > name]: class: nameContent was not found in html')
            game_name = None

        # Get the price of the game
        # - Find the class selected-price
        # - Check if it exists
        #   - Get the rext
        #       - Remove the euro sign (\u20AC)
        price = soup.find(class_='selected-price')
        if price:
            price = price.get_text(strip=True).replace('\u20AC', '')  
        else:
            print('[CRAWLER > G2a > game > price]: class: selected-price was not found in html')
            price = None
            
    
        # Get the description of the game
        # - Find class prodDetailsText
        # - Check if it is bigger than or equal to 1 (=> it has results)
        #   - Find the p in the first ([0]) result
        #   - Check if the p exists
        #       - Get the text
        #       - Get the stripped text
        desc = soup.find_all(class_='prodDetalisText')
        if len(desc) >= 1:
            desc = desc[0].find('p')
            if desc:
                raw_desc = desc.get_text()
                desc = raw_desc.strip()
            else:
                print('[CRAWLER > G2a > game > desc]: p was not found in desc[0]')
                desc = None
        else:
            print('[CRAWLER > G2a > game > desc]: class: prodDetalisText was not found in desc[0]')

        
        # Get the game's main image
        # - Find class games-image
        # - Check if it has results
        #   - Find img
        #   - Check if img exists
        #       - Check if source exists
        #       - Extract source
        img = soup.find_all(class_='games-image')
        if len(img) >= 1:
            img = img.find('img')
            if img:
                if 'src' in img:
                    img = img['src']
                else:
                    print('[CRAWLER > G2a > game > img]: src was not found in img')
                    img = None
            else:
                print('[CRAWLER > G2a > game > img]: tag img was not found in img[0]')
                img = None
        else:
            print('[CRAWLER > G2a > game > img]: class: games-image was not found in html')            
            img = None
        
        # Get slider images
        # - Find class cw-img-list
        # - Check if it has results
        #   - Find all li
        #   - Check if it exists
        #   - Loop trough the lis
        #       - Per li find img
        #           - Check if img exists
        #               - Check if img has key src
        #                   - Extract src
        slider = soup.find_all(class_='cw-img-list')
        if len(slider) >= 1:
            slider = slider[0].find_all('li')
            if len(slider) >= 1:
                img_slider = []
                for li in slider:
                    li_img = li.find('img')
                    if 'src' in li_img:
                        img_slider.append(li_img['src'])
                    else:
                        print('[CRAWLER > G2a > game > img_slider]: li_img has no attribute src')
            else:
                print('[CRAWLER > G2a > game > img_slider]: tag li was not found in slider[0]')
        else:   
            print('[CRAWLER > G2a > game > img_slider]: class: cw-img-list was not found in html')
            img_slider = None 

        result = {
            'name'      : name,
            'desc'      : desc,
            'raw_desc'  : raw_desc,
            'img'       : img,
            'slider_img': img_slider,
            'price'     : price
        }                

        return result


    @staticmethod
    def search(self, query, url=G2A_DEFAULT_SEARCH_URL):
        '''
        Search g2a for query and return the results
        Args:
            query (str): The query to search for
            url (str) (default: The standart search url): The url to the search page (/api)
        Return:
            (list) search_results: Contains dicts containing search results information
        Raises:
            CrawlUrlError: When the url is invalid
            CrawlRequestError: When the request failed
            CrawlDataError: When there was no data returd
        '''

        # Define search_results to never fail return
        search_results = []
        
        # Validate the url
        # If invalid raise CrawlUrlError
        validate_url(url)

        # Handle the request 
        # We are not using the get_html function
        # because we use g2a's internal api, which returns json
        # and it requires some special formatting to be valid json
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            data = r.text[1:-1]
        else:
            raise CrawlRequestError('Request to url: {}, failed with code {}'.format(url, r.status_code))

        # Validate the data
        # - Check if it exists
        #   - Check if it is a str
        #       - Convert it to json obj
        if data is not None:
            if isinstance(data, str):
                try:
                    json_data = json.loads(data)
                except JSONDecodeError as exep:
                    raise CrawlDataError('Failed to decode to json with JSONDecodeError: {}'.format(exep))
                
            else:
                raise CrawlDataError('Data returned by request is not a valid str')
        else:
            raise CrawlDataError('Data returned by request does not exist')
        

        # Extract the results from the json_data
        # - Check if docs exists in the dat
        #   - Loop trough the results[docs]
        #       - For result check if name exists
        #       - Check if price exists
        #       - Check if slug exists
        #       - Check if smallImage exists
        if 'docs' in json_data:
            results = json_data['docs']
            for result in results:
                if 'name' in result:
                    name = result['name']
                else:
                    name = None
                    print('[CRAWLER > G2a > search > name]: name could not be found for current result')
                
                if 'minPrice' in result:
                    price = result['minPrice']
                else:
                    price = None
                    print('[CRAWLER > G2a > search > price]: price could not be found for current result')
                
                if 'slug' in result:
                    slug = result['slug']
                    url = 'https://g2a.com{}'.format(slug)
                else:
                    slug = None
                    url = None
                    print('[CRAWLER > G2a > search > slug]: slug could not be found for current result')

                if 'smallImage' in result:
                    small_img = result['smallImage']
                else:
                    small_img = None
                    print('[CRAWLER > G2a > search > smallImage]: smallImage could not be found for current result')
                
                current_result = {
                    'name'      : name,
                    'price'     : price,
                    'url'       : url,
                    'small_img' : small_img
                }

                search_results.append(current_result)

        else:
            print('[CRAWLER > G2a > search > json_data]: docs could not be found in json_data')

        return search_results

class Kinguin:
    ''' ''''

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
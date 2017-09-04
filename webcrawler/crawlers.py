'''
All the crawlers for crawling the sites we need for our site
G2a - Crawl g2a.com
    - Games: Crawls the game page
    - Search: Crawl the search page

Kinguin - Crawl kinguin.net
    - Games: Crawls the game page
    - Search: Crawls the search page

Gamestop - Crawl gamestop.com
    - Games: Crawl the game page
    - Search: Crawl the search page

Gameranking - Crawl gameranking.com for rankings for games
    - game_ranking: Crawl the ranking page for a game
    - search_raking: Crawls the search page
        - Returns the fist search result

Reddit - Crawl reddit to gain community urls
    - community_url: Crawl reddit search to find subreddits
        - Returns the subreddits url as community url

'''

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
    def game(url):
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
        soup = BS(get_html(url), 'lxml')

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
                if 'src' in img.attrs:
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
                    if 'src' in li_img.attrs:
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
    def search(query, url=G2A_DEFAULT_SEARCH_URL):
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
        
        # Format the query to fit the url
        query = query.replace(' ', '+')

        # Create the url with the query        
        url = url.format(query)

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
    ''' Webcrawler for kinguin.net '''

    @staticmethod
    def game(url):
        '''
        Crawl kinguin.nets game's page
        and extract all relevant information about the game from the page.
        Args:
            url (str): The url to the game's page
        Returns:
            (dict) The relevant information
                'name': 'The name of the game',
                'desc': 'Game description',
                'img_url': 'The url to the main img',
                'sys_req': 'The system requirements of the game',
                'price': 'The price of the game'
        Raises:
            CrawlUrlError: If the url is invalid
            CrawlRequestError: If the request failed
        '''
        
        # Validate the url
        # If the validation failes
        # Raise CrawlUrlError
        validate_url(url)

        # Create the results dict to always return something
        result = {}

        # Declare all the return variables
        # We do this because we do not want
        # to return a not declared variable.
        # This way we will always return something
        # even if it does not exist - None
        name    = None
        desc    = None
        img_url = None
        sys_req = None
        price   = None
    
        # Create the bs4 soup object with the requests html data
        # If the request fails raise CrawlRequestError
        soup = BS(get_html(url), 'lxml')

        # Get the name of the game
        # - Find class product-name
        # - Check if it exists
        #   - Get the stripped text
        name = soup.find(class_='product-name')
        if name:
            name = name.get_text(strip=True)
        else:
            name = None
            print('[CRAWLER > Kinguin > game > name]: class: product-name could not be found in html')
        
        # Get the price of the game
        # - Find class category-page__price--price
        # - Check if it exists
        #   - Get the stripped text
        price = soup.find(class_='category-page__price--price')
        if price:
            price = price.get_text(strip=True)
        else:
            print('[CRAWLER > Kinguin > game > price]: class: category-page__price--price could not be found in html')
            price = None
        
        # Get the description of the game
        # - Find class category-page__category-description
        # - Check if it exists
        #   - Find p tag
        #   - Check if the p exists
        #       - Get the stripped text
        desc = soup.find(class_='category-page__category-description')
        if desc:
            desc = desc.find('p')
            if desc:
                desc = desc.get_text(strip=True)
            else:
                desc = None
                print('[CRAWLER > Kinguin > game > desc]: Could not find p tag')
        else:
            desc = None
            print('[CRAWLER > Kinguin > game > desc]: class: category-page__category-description could not be found in html')
        
        # Get the system requirements for the game
        # - Find class category-page__category-description
        # - Check if it exits
        #   - Find ul tag
        #   - Check if it exists
        #       - Take the seccond [1] entry
        #       - Get the stripped text
        sys_req = soup.find(class_='category-page__category-description')
        if sys_req:
            sys_req = sys_req.find_all('ul')
            if len(sys_req) >= 2:
                sys_req = sys_req[1].get_text(strip=True)
            else:
                sys_req = None
                print('[CRAWLER > Kinguin > game > sys_req]: Not enough uls found in class category-page__category-description')
        else:
            sys_req = None
            print('[CRAWLER > Kinguin > game > sys_req]: Could nog find class category-page__category-description')
        
        # Get the main image of the game
        # - Find class category-page__main-image-wrapper
        # - Check if it exists
        #   - Find img tag
        #   - Check if it exists
        #       - Check if it has a src 
        #           - Get the src
        img_url = soup.find('category-page__main-image-wrapper')
        if img_url:
            img_url = img_url.find('img')
            if img_url:
                if 'src' in img_url.attrs:
                    img_url = img_url['src']
                else:
                    img_url = None
                    print('[CRAWLER > Kinguin > game > img_url]: Could not find src of img')
            else:
                img_url = None
                print('[CRAWLER > Kinguin > game > img_url]: Could not find img tag in class category-page__main-image-wrapper')
        else:
            img_url = None
            print('[CRAWLER > Kinguin > game > img_url]: Could not find class category-page__main-image-wrapper')
        

        result = {
            'name': name,
            'desc': desc,
            'img_url': img_url,
            'sys_req': sys_req,
            'price': price
        }

        return result

    @staticmethod
    def search(query, url=KINGUIN_DEFAULT_SEARCH_URL):
        '''
        Crawl the search page for the given query and return all teh results
        Args:
            query (str): The query to search for
            url (str) (default: The standart search url): The url that points to the search page
        Returns:
            (list) search_results contains the search results formatted in dics with keys:
                [{
                    'name'          : 'The results name',
                    'official_price': 'The official price of the game',
                    'price'         : 'The price of the game',
                    'url'           : 'The url to the game page',
                    'img_url'       : 'The url to the games imgage'
                }]
        Raises:
            CrawlUrlError: When the url is invalid
            CrawlRequestError: When the request failed
        '''

        # Create the default return list
        # We append to this later, and we always have a list ready for return
        search_results = []

        # Format the query to fit the url
        query = query.replace(' ', '+')
        # Create the url with the query
        url = url.format(query)

        # Check if the url is valid
        # If it is not valid we raise a CrawlUrlError
        validate_url(url)

        # Create a beautifull soup obj
        # We do this using requests to get the html
        # If the request failes we raise a CrawlRequestError
        soup = BS(get_html(url))

        # Find the dictionary containing the results
        # And check if it exists
        offerDetails = soup.find(id='offerDetails')
        if offerDetails:
            # Find all rows in offer details
            # And check if they exist
            rows = offerDetails.find_all(class_='row')
            if len(rows) >= 1:
                # Loop trough rows
                # And extract all the data from it
                for row in rows:
                    game_name = row.find(class_='product-name')
                    if game_name:
                        game_name = game_name.find('a')
                        if game_name:
                            game_name = game_name.get_text()
                        else:
                            game_name = None
                            print('[CRAWLER > Kinguin > search > game_name]: Could not find the a tag')
                    else:
                        game_name = None
                        print('[CRAWLER > Kinguin > search > game_name]: Could not find product-name in row')
                    
                    prices = row.find(class_='new-price')
                    if prices:
                        official_price = prices.find(class_='official-price')
                        if official_price:
                            official_price = official_price.find_all('span', class_='price')
                            if len(official_price) >= 1:
                                official_price = official_price[1].get_text(strip=True).replace('\u20ac', '')
                            else:
                                official_price = None
                                print('[CRAWLER > Kinguin > search > price]: Could not find the [1] span with class price')
                        else:
                            official_price = None
                            print('[CRAWLER > Kinguin > search > price]: could not find class official-price')
                        
                        offered_price = prices.find(class_='actual-price')
                        if offered_price:
                            offered_price = offered_price.find('span')
                            if 'data-no-tax-price' in offered_price.attrs:
                                offered_price = offered_price['data-no-tax-price']
                            else:
                                offered_price = None
                                print('[CRAWLER > Kinguin > search > price]: could not find data-no-tax-price key for actual price')
                        else:
                            offered_price = None
                            print('[CRAWLER > Kinguin > search > price]: Could not find actual price class')

                url = row.find(class_='product-name')
                if url:
                    url = url.find('a')
                    if 'href' in url.attrs:
                        url = url['href']
                    else:
                        url = None
                        print('[CRAWLER > Kinguin > search > url]: could not find href for a')
                else:
                    url = None
                    print('[CRAWLER > Kinguin > search > url]: Could not find class product-name ')
                           
                img_url = row.find(class_='main-image')
                if img_url:
                    img_url = img_url.find('img')
                    if 'src' in img_url.attrs:
                        img_url = img_url['src']
                    else:
                        img_url = None
                        print('[CRAWLER > Kinguin > search > img_ur]: could not find src for img tag')
                else:
                    img_url = None
                    print('[CRAWLER > Kinguin > search > img_url]: could not find class main-image')

                current_game = {
                    'name'          : name,
                    'official_price': official_price,
                    'price'         : offered_price,
                    'url'           : url,
                    'img_url'       : img_url
                }
                search_results.append(current_game)

        return search_results
                        
                        
class Gamestop:
    ''' Webcrawler for gamestop.com '''

    @staticmethod
    def game(url):
        '''
        Crawl the game page (url) and extract relevant inforamtion to display on the games page
        Args:
            url (str): The url of the game
        Returns:
            (dict) The relevant inforamtion extracted
                'name': game_name,
                'price': game_price,
                'desc': game_desc,
        Raises:
            CrawlUrlError: When the url was not valid
            CrawlRequestError: When the request went wrong
        '''
        
        # Validate the url
        # If the url is invalid raise CrawlUrlError
        validate_url(url)

        # Create the return dictionary
        result = {}

        # Declare all the retur variables
        # So they will always exist,
        # even if they are not found while crawlign the page
        name = None
        disc_price = None
        online_price = None
        price = None
        desc = None

        # Create bs4 soup obj from html returend by requests
        # If request failes CrawRequestError is raised
        soup = BS(get_html(url))

        # Get the name of the game
        # - Find class ats-prod-title
        # - Check if it exists
        #   - Extract the text from it
        name = soup.find(class_='ats-prod-title')
        if name:
            name = name.get_text(strip=True)
        else:
            name = None
            print('[CRAWLER > Gamestop > game > name]: could not find class ats-prod-title')

        # Get the prices for the game
        # - Find the class ats-prodBuy-price
        # - Check if it exists
        #   - 0 - the discprice
        #   - 1 - the online price
        prices = soup.find_all(class_='ats-prodBuy-price')
        if len(prices) >= 2:
            disc_price = prices[0]
            online_price = prices[1]
            price = min([disc_price, online_price])
        else:
            price = None
            print('[CRAWLER > Gamestop > game > price]: could not find class ats-prod-Buy-price, or it did not have enough values')

        # Get the desc for the game
        # - Find class longdescription
        # - Check if it exists
        #   - Extract the text from it
        desc = soup.find(class_='longdescription')
        if desc:
            desc = desc.get_text(strip=True)
        else:
            desc = None
            print('[CRAWLER > Gamestop > game > desc]: could not find class longdescription')
        
        result = {
            'name': name,
            'price': price,
            'desc': desc
        }

        return result

    @staticmethod
    def search(query, url=GAMESTOP_DEFAULT_SEARCH_URL):
        '''
        Acces the search page of gamestop and search the given query.
        Args:
            query (str): The query to search
            url (str): The url to the search page
        Returns:
            results (list): The results found
        Raises:
            CrawlUrlError: When the url is invalid
            CrawlRequestError: When the request failed
        '''

        # Create empty return obj
        # This way we always have something to return
        search_results = []

        # Format query to fit the url
        # Replace spaces with +
        query = query.replace(' ', '+')

        # Format url with the query
        url = url.format(query)
        
        # Validate url
        # If the validation fails
        # we raise CrawlUrlError
        validate_url(url)

        # Create a bs4 soup obj from the requests html
        # If the request failes we raise a CrawlRequestError
        soup = BS(get_html(url),'lxml')

        # Find all products
        # - Find all class product
        # - Check if the products list exists
        results = soup.find_all(class_='product')
        if results >= 1:

            # Loop trough the results
            # And extract all the data 
            for result in results:
                name = result.find('h3')
                if name:
                    name = name.find('a')
                    if name:
                        name = name.get_text(strip=True)
                    else:
                        name = None
                        print('[CRAWLER > Gamestop > search > name]: could not find a in h3')
                else:
                    name = None
                    print('[CRAWLER > Gamestop > search > name]: could not find h3')
        
                price = result.find(class_='purchase_info')
                if price:
                    price = price.get_text(strip=True)
                else:
                    price = None
                    print('[CRAWLER > Gamestop > search > price]: could not find class purchase info')
                
                url = result.find('h3')
                if url:
                    url = url.find('a')
                    if 'href' in url.attrs:
                        url = url['href']
                    else:
                        url = None
                        print('[CRAWLER > Gamestop > search > url]: url has not attribute href')
                else:
                    url = None
                    print('[CRAWLER > Gamestop > search > url]: could not find h3')
            
                search_results.append(
                    {
                        'name': name,
                        'price': price,
                        'url': url
                    }
                )

        return search_results


class Gameraking:
    ''' Webcrawler for gameranking.com '''

    @staticmethod
    def game_rating(url):
        '''
        Get the rating for a game
        Args:
            game_url (str): The url to the game to get the rating of
        Returns:
            rating (str): The rating percentage
        Raises:
            CrawlUrlError: when the url is not valid
            CrawlRequestError: when the request failed
        '''
        
        # Declare return variable
        rating = None

        # Validate url
        # If url is not valid raise CrawlUrlError
        validate_url(url)

        # Create soup Bs object from requests html
        # If the request failes raise CrawlRequestError
        soup = BS(get_html(url), 'lxml')

        # Get the rating
        # - Find the id main-col
        # - Check if it exists
        #   - Find all tables
        #   - Check if tables exists
        #       - Find span in table[0]
        #       - Check if the span exists
        #           - Take the text
        #           - Format the text
        rating = soup.find(id='main_col')
        if rating:
            rating = rating.find_all('table')
            if len(rating) >= 1:
                rating = rating[0].find('span')
                if rating:
                    # Remove the % sign
                    rating = rating.get_text(strip=True)[:-1]
                else:
                    print('[CRAWLER > Gamerating > game_rating > rating]: Could not find the span')
            else:
                print('[CRAWLER > Gamerating > game_rating > rating]: Could not find the table')
        else:
            print('[CRAWLER > Gamerating > game_rating > rating]: could not find main_col')
            
                    
        return rating
    
    @staticmethod
    def search_rating(query, url=GAMERANKING_DEFAULT_SEARCH_URL):
        '''
        Search gameranking's pc games for the query and return its page and rating
        Args:
            query (str): The query to search for
            url (str) (default: The default url): The url to the search page
        Returns:
            result (list): A dictionary containing the result
                [0]: the url to the page
                [1]: The rating
        Raises:
            CrawlURLError: When the url is not valid
            CrawlRequestError: When the request failed            
        '''
        
        # Declare the vaiables that will be returned
        url = None
        rating = None

        # Format the query to fit the url
        query = query.replace(' ', '+')
        
        # Format the url (place the query in it)
        url = url.fomat(query)

        # Validate the url
        # If the url is not valid raise CrawlUrlError
        validate_url(url)

        # Create the BS soup obj, fill it with requests html
        # If the request failes we raise the CrawlRequestError
        soup = BS(get_html(url), 'lxml')

        # Get the url of the first game
        # - Find table
        # - Check if table exists
        #   - Find all a tags
        #   - Check if the a tags exists
        #       - Check if [0][href] exists
        #       - Get the [0][href]
        url = soup.find('table')
        if url:
            url = url.find_all('a')
            if len(url) >= 1:
                url = url[0]
                if 'href' in url.attrs:
                    url = url['href']
                else:
                    url = None
                    print('[CRAWLER > Gamerating > search > url]: A tag did not have href')
            else:
                print('[CRAWLER > Gamerating > search > url]: Could not find a tag')
        else:
            print('[CRAWLER > Gamerating > search > url]: could not find table')


        rating = soup.find('table')
        if rating:
            rating = rating.find_all('span')
            if len(rating) >= 1:
                rating = rating[0].get_text(stip=True)[:-1]
            else:
                rating = None
                print('[CRAWLER > Gamerating > search > rating]: could not find span')
        else:
            rating = None
            print('[CRAWLER > Gamerating > search > rating]: could not find table')

        return [url, rating]
        

class Reddit:
    ''' Webcrawler for reddit '''

    @staticmethod
    def get_community_url(query, url=REDDIT_SEARCH_URL):
        '''
        Get the url to the community page for the queried game
        Args:
            query (str): The query/game to search for
            url (str) (default: default reddit search_url): The url to the reddit search page
        Returns:
            community_url (str): the url to the queries/games community subreddit on reddit
        Raises:
            CrawlUrlError: When the url is invalid
            CrawlRequestError: When the request failed
        '''
        # Declare return variable
        community_url = None

        # Format query to fit the url
        query = query.replace(' ', '+')
        
        # Fit the query in the url
        url = url.format(query)

        # Validate url
        # If the validation failes CrawlUrlError is thrown
        validate_url(url)

        # Get the html from the url and create a bs4 soup obj with it
        soup = BS(get_html(url), 'lxml')

        # Get the community url
        # - Find all classes search-result-header
        # - Check if it exists
        #   - Find an a tag on the [0] element
        #   - Check if the a tag exists
        #       - Check if the href exists
        #       - Get the href
        community_url = soup.find_all(class_='search-result-header')
        if len(community_url) >= 1:
            community_url = community_url[0]
            community_url = community_url.find('a')
            if community_url:
                if 'href' in community_url.attrs:
                    community_url = community_url['href']
                else:
                    print('[CRAWLER > Reddit > search > community url]: Could not find href in a tag')
            
            else:
                print('[CRAWLER > Reddit > search > community url]: Could not find a')

        else:
            print('[CRAWLER > Reddit > search > community url]: Could not find search-result-header ')
            
                    

        # Return the community url
        return community_url

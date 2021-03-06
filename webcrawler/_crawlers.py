import json
from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup as bs

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import requests

URL_VALIDATOR = URLValidator()

G2A_DEFAULT_SEARCH_URL = 'https://g2a.com/lucene/search/filter?jsoncallback=&skip=&minPrice=0.00&maxPrice=1422.00&cc=NL&stock=all&event=&search={}&genre=0&cat=0&sortOrder=popularity+desc&start=0&rows=12&steam_app_id=&steam_category=&steam_prod_type=&includeOutOfStock=false&includeFreeGames=false&isWholesale=false&_=1503469082372'

KINGUIN_DEFAULT_SEARCH_URL = 'https://www.kinguin.net/catalogsearch/result/index/?p=1&q={}&order=bestseller&dir=desc&max_price=143&dir_metacritic=desc&hide_outstock=1'

GAMESTOP_DEFAULT_SEARCH_URL = 'http://www.gamestop.com/browse/pc?nav=16k-3-{},28-wa2,138c'

GAMERANKING_DEFAULT_SEARCH_URL = 'http://www.gamerankings.com/browse.html?search={}&numrev=3&site=pc'

REDDIT_SEARCH_URL = 'https://www.reddit.com/search?q={}'


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


class G2a:
    '''Webcrawler for g2a.com'''

    def __init__(self, search_url):
        ''' Retrieve some basic variables '''
        self.SEARCH_BASE_URL = search_url

    def game(self, url):
        '''
        Crawl the game's page (url) and extract relevant information to display on the site

        Args:
            url: (str) The url of the game
        Returns:
            (dict) The relevant information
                'name':       game_name,
                'desc':       game_desc,        
                'desc_text':  game_desc_text,
                'img':        game_img_url,
                'slider_img': game_slider_img_url,
                'price':      game_selected_price
        Raises:
            CrawlRequestError: When the request went wrong
            CrawlDataError: When there is a problem with the data
        '''

        # Check if the url is a valid url
        # We do this to ensure that we will request a good url
        # And to save data/resources when handleling a lot of requests
        try:
            URL_VALIDATOR(url)
        except ValidationError:
            raise CrawlUrlError('No valid url')
        
        # Variable delcaration
        game_name = None
        game_selected_price = None
        game_desc = None
        game_desc_text = None
        game_img_url = None
        game_slider_img_url = None

        r = requests.get(url)

        # We check if the request wa sucessfull,
        # If it was sucess full we create the data variable which holds the returned content
        if r.status_code == requests.codes.ok:
            data = r.text
        else:
            data = None
            # Raise a CrawlRequestError
            raise CrawlRequestError('Request had code: {} and failed'.format(r.status_code))

        # We create a soup obj from the data returned from the request
        # Lxml is used by bs to parse the html
        soup = bs(data, 'lxml')

        # Get the game title
        # find the <div class='nameContent>
        # The divs only child is a h1 which we select with .contents
        # We extract the value of the h1 with .string
        game_name = None
        game_name = soup.find_all(class_='nameContent')[0].find('h1').get_text().strip()
        
        # Get the selected price (tag; div)
        # We extract the value by using the .get_text()
        # We use .strip() to get rid of exta spaces
        game_selected_price = soup.find(class_='selected-price').get_text().replace('\u20AC', '').strip()

        # Get the game description
        # Find <div class='prodDetalisText'> the first one is the description
        # Find the <p> containing the description
        # The <p> contains tags like <strong> therefore we create a text only version
        # Then we save the non text only's content
        game_desc = soup.find_all(class_='prodDetalisText')[0]
        game_desc = game_desc.find('p')
        game_desc_text = game_desc.get_text()
        game_desc = game_desc.get_text().strip()

        # Get all the slider images
        # The images are held in a ul which contains li's with img[src] containing the url
        slider = soup.find_all(class_='cw-img-list')[0]
        game_slider_lis = slider.find_all('li')
        game_slider_img_url = []
        for li in game_slider_lis:
            img = li.find('img')['src']
            game_slider_img_url.append(img)
        
        # Get the games image url
        # Find the <div class='games-image'> 
        # Get the <img src=x> and extract the src [src]
        game_img_url = soup.find_all(class_='games-image')[0] # TODO check if the [0] matters
        game_img_url = game_img_url.find('img')['src']

        result = {
            'name':       game_name,
            'desc':       game_desc,        
            'desc_text':  game_desc_text,
            'img':        game_img_url,
            'slider_img': game_slider_img_url,
            'price':      game_selected_price
        }

        return result

    def search(self, query):
        '''
        Crawl g2a search to return the results of the search

        Args:
            query: (str) Search query
        Returns:
            (list) The results
        Raises:
            CrawlRequestError: When the request went wrong
            CrawlDataError: When there is a problem with the data
        '''

        # This list is used to store the results
        # This list is returend at the end of this function
        results = []

        # Combine the user specified search query with the already predifinced url of g2a search api
        query = query.replace(' ', '+')
        url = self.SEARCH_BASE_URL.format(query)

        # We use requests to 'request' the url and therefore return the content of the search
        r = requests.get(url)

        # We check if the request wa sucessfull,
        # If it was sucess full we create the data variable which holds the returned content
        if r.status_code == requests.codes.ok:

            # We coould use r.json but we dont 
            # because the api adds () to the response
            # because of this same reason we remove the first and last character of the response data
            data = r.text[1:-1]

        else:
            data = None
            # Raise a CrawlRequestError
            raise CrawlRequestError('Request went wrong with code: {}'.format(r.status_c))
            

        # Check if data is valid
        # So, data has to exist and be valid json
        if data is not None:
            if isinstance(data, str):
                try:
                    #  Convert the string from r.text to a python interpretable dict
                    json_data = json.loads(data)

                # We create an exeption for JSONDecodeError
                # The JSONDecodeErro can ocur in json.loads 
                # when the string is not utf-8
                # It is appropiate to use here because we do not control the source
                # of the string and therefor is is subject to change 
                except JSONDecodeError as exep:
                    raise CrawlDataError('JSONDecodeError: {}'.format(exep))
            else:
                # Data is not a string
                raise CrawlDataError('Data inputed is not of type str')
        else:
            # When the data is none, non-existent
            raise CrawlDataError('Data is not existent')


        # Extract the actual games from the results
        # By looping over all the games 
        # For everygame we extract the name, price, slug and the small_img
        # This gets combined in a new dictionary that gets added to the results list
        games = json_data['docs'] 
        for game in games:
            game_name = game['name']
            price = game['minPrice']
            slug = game['slug']
            url = 'https://g2a.com{}'.format(slug)
            small_img = game['smallImage']

            current_game = {
                'name': game_name,
                'price': price,
                'url': url,
                'small_img': small_img
                }
            
            # Return
            results.append(current_game)

        return results

class Kinguin:
    ''' Webcrawler for kinguin.net '''

    def __init__(self, search_url):
        ''' Retreive some basic variables and store them in the class scope  '''
        self.SEARCH_BASE_URL = search_url

    def game(self, url):
        '''
        Crawl the page of a certain game for relevant inforamtion

        Args:
            url: (str) The url to the specifics game's page
        Returns:
            (dict) The relevant information
                 'name': game_name,
                 'desc': game_desc,
                 'img_url': game_img_url,
                 'sys_req': game_sys_req,
                 'price': game_price
        Exceptions:
            CrawlRequestError: When the request failed
        ''' 

        try:
            URL_VALIDATOR(url)
        except ValidationError:
            raise CrawlUrlError('No valid url')

        result = {}
        
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            html = ''
            raise CrawlRequestError('Request went wrong with code: {}'.format(r.status_c))

        game_name = None
        game_desc = None
        game_img_url = None
        game_price = None
        game_sys_req = None
        soup = bs(html, 'lxml')

        game_name = soup.find(class_='product-name').text.strip()
        game_price = soup.find(class_='category-page__price--price').text.strip().replace('\u20ac', '')
        game_desc = soup.find(class_='category-page__category-description').find('p').text.strip()
        # game_sys_req = soup.find(class_='category-page__category-description').find_all('ul')[1].text.strip()
        game_img_url = soup.find(class_='category-page__main-image-wrapper').find('img')['src']



        result = {
            'name': game_name,
            'desc': game_desc,
            'img_url': game_img_url,
            # 'sys_req': game_sys_req,
            'price': game_price
        }

        return result
        

    def search(self, query):
        '''
        Crawl, the search page for the given query and return all the results with relevant information
        Args:
            query: (str) The query to use to search (probably user submitted)
        Return:
            (list) Returns a list of dictionaries containing all the results with the relevant information in the dictionaries
        Exceptions:        
            CrawlRequestError: When the request to the url went wrong
        '''
        
        # The list that will be returned containing dictionaries with the search results
        results = []

        # Replace spaces in query with +
        # Create the full url to the search page
        query = query.replace(' ', '+')
        url = self.SEARCH_BASE_URL.format(query)
        
        # Uses request to request the url
        r = requests.get(url)

        # Check the status code 
        # To check if the request was sucessfull
        # If the request failed return a CrawlRequestError
        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            html = ''
            raise CrawlRequestError('Request went wrong with code: {}'.format(r.status_c))
        
        # Convert the html into a beautifull soup obj
        soup = bs(html, 'lxml')

        # Find the div with id=offerDetails
        offerDetails = soup.find(id='offerDetails')
        # Find all rows (dict)
        rows = offerDetails.find_all(class_='row')

        # Loop through the rows and extract information
        for row in rows:

            # Try block to catch AttributeError s
            # AttributeError occurs sometime when a tag is not found but still .find 
            # Is used on the tag, in that case we do not want to stop the whole crawler
            try:
                img_url = row.find(class_='main-image').find('img')['src']
                game_name_a = row.find(class_='product-name').find('a')
                game_name = game_name_a.text.strip()
                game_url = game_name_a['href']
                prices = row.find(class_='new-price')
                official_price = prices.find(class_='official-price').find_all('span', class_='price')[1].text.strip().replace('\u20ac', '')
                offered_price = prices.find(class_='actual-price').find('span')['data-no-tax-price']
            except AttributeError:
                pass
            
            # Add all the inforamtion into a dict
            # Then append the dict to the results list
            current_game = {
                'name': game_name,
                'official_price': official_price,
                'offered_price': offered_price,
                'url': game_url,
                'img_url': img_url,
            }
            results.append(current_game)

        return results


class GreenmanGaming:

    def __init__(self, search_url):
        ''' 
        Retrieve basic variables and store them in self
        Args:
            search_url (str): The url to the search page of greenman gaming
        '''
        self.SEARCH_BASE_URL = search_url

    
    def game(self, url):
        '''
        Crawl the game's page (url) and extract relevant information to display on the site
        Args:
            url: (str) The url of the game
        Returns:
            (dict) The relevant information
                'name':       game_name,
                'price':      game_selected_price
                'rating':      rating of greenman gaming
        Raises:
            CrawlRequestError: When the request went wrong
            CrawlDataError: When there is a problem with the data
        '''

        try:
            URL_VALIDATOR(url)
        except:
            raise CrawlUrlError('URL: {} is not valid'.format(url))

        result = {}

        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            raise CrawlRequestError('Request failed, with codoe {}'.format(r.status_code))

        game_name = None
        game_price = None
        game_rating = None

        game_script = None

        soup = bs(html, 'lxml')
        

        scripts = soup.find_all('script')
        for script in scripts:
            if 'var game' in script.text:
                game_script = script
        
        return result


class Gamestop:
    ''' Webcrawker for gamestop '''

    def __init__(self, search_url):
        '''
        Retrieve and store some basic variables
        Args:
            search_url (str): The url that turns to the search page
        '''
        self.SEARCH_URL = search_url

    def game(self, url):
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
        try:
            URL_VALIDATOR(url)
        except ValidationError:
            raise CrawlUrlError('Url {} was not valid'.format(url))

        result = {}

        game_name = None
        game_disc_price = None
        game_online_price = None
        game_price = None
        game_desc = None
        
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            raise CrawlRequestError('Request failed with code {}'.format(r.status_code))
        
        soup = bs(html, 'lxml')

        game_name = soup.find(class_='ats-prod-title').text.strip()

        prices = soup.find_all(class_='ats-prodBuy-price')

        game_disc_price = prices[0]
        game_online_price = prices[1]

        game_desc = soup.find(class_='longdescription').text.strip()

        game_price = min([game_disc_price.text, game_online_price.text])

        result = {
            'name': game_name,
            'price': game_price,
            'desc': game_desc,
            }

        return result




    def search(self, query):
        '''
        Acces the search page of gamestop and search the given query.
        Args:
            query (str): The query to search
        Returns:
            results (list): The results found
        Raises:
            -
        '''

        results = []
        
        query = query.replace(' ', '+')
        url = self.SEARCH_URL.format(query)

        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            raise CrawlRequestError('Request failed with code {}'.format(r.status_code))

        soup = bs(html, 'lxml')

        search_results = soup.find_all(class_='product')
        
        for result in search_results:
            result_name = result.find('h3').find('a').text.strip()
            result_price = result.find(class_='purchase_info').text.strip()
            result_url = result.find('h3').find('a')['href']
            results.append(
                {
                    'name': result_name,
                    'price': result_price,
                    'url': result_url
                }
            )
        
        return results


class GameRanking:
    ''' Crawler for gameranking.com '''

    def __init__(self, search_url):
        self.SEARCH_URl = search_url

    def rating(self, game_url):
        '''
        Get the rating for a game
        Args:
            game_url (str): The url to the game to get the rating of
        Returns:
            rating (str): The rating percentage

        '''

        try:
            URL_VALIDATOR(game_url)
        except ValidationError:
            raise CrawlUrlError('Url {} is not a valid url'.format(game_url))
        
        r = requests.get(game_url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            raise CrawlRequestError('Request failed with code {}'.format(r.status_code))
        
        soup = bs(html, 'lxml')

        rating = None

        rating = soup.find(id='main_col').find_all('table')[0].find('span').text.strip()[:-1]

        return rating
    
    def search_rating(self, query):
        '''
        Search gameranking's pc games for the query and return its page and rating
        Args:
            query (str): The query to search for
        Returns:
            result (dict): A dictionary containing the result
                [0]: the url to the page
                [1]: The rating
        Raises:
            CrawlURLError: When the url is not valid
            CrawlRequestError: When the request failed            
            CrawlDataError: When there is no search result for query
        '''

        query = query.replace(' ', '+')

        url = self.SEARCH_URl.format(query)

        try:
            URL_VALIDATOR(url)
        except ValidationError:
            raise CrawlUrlError('The url {} is not valid'.format(url))
        
        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            raise CrawlRequestError('Request failed with code {}'.format(r.status_code))

        soup = bs(html, 'lxml')

        try:
            first_result_url = soup.find('table').find_all('a')[0]['href']
            first_result_rating = soup.find('table').find_all('span')[0].text.strip()[:-1]
        except Exception as e:
            raise CrawlDataError('No search results found for {} on {} therefore error: {}'.format(query, url, e))
        return [first_result_url, first_result_rating]


class Reddit:
    def __init__(self, search_url):
        self.SEARCH_URL = search_url

    def get_community(self, query):

        query = query.replace(' ', '+')
        url = self.SEARCH_URL.format(query)

        try:
            URL_VALIDATOR(url)  
        except ValidationError:
            raise CrawlUrlError('Url {} is not valid'.format(url))

        r = requests.get(url)

        if r.status_code == requests.codes.ok:
            html = r.text
        else:
            raise CrawlRequestError('Request failed with code {}'.format(r.status_code))

        
        soup = bs(html, 'lxml')

        community_url = soup.find_all(class_='search-result-header')[0].find('a')['href']

        return community_url
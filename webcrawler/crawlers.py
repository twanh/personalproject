import json
from json.decoder import JSONDecodeError

from bs4 import BeautifulSoup as bs

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import requests

URL_VALIDATOR = URLValidator()

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

    def game(self, url):
        '''
        Crawl the game's page (url) and extract relevant information to display on the site

        Args:
            url: (str) The url of the game
        Returns:
            (dict) The relevant information
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
        url = 'https://g2a.com/lucene/search/filter?jsoncallback=&skip=&minPrice=0.00&maxPrice=1422.00&cc=NL&stock=all&event=&search={}&genre=0&cat=0&sortOrder=popularity+desc&start=0&rows=12&steam_app_id=&steam_category=&steam_prod_type=&includeOutOfStock=false&includeFreeGames=false&isWholesale=false&_=1503469082372'.format(query)

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
            raise CrawlRequestError('Request had code: {} and failed'.format(r.status_code))

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



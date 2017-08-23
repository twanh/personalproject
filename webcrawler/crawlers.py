import json

import requests

class CrawlRequestError(Exception):
    ''' 
    Raise when something goes wrong while crawling a page
    specificly when the request goes wrong. 
    '''
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

        '''

    def search(self, query):
        '''
        Crawl g2a search to return the results of the search

        Args:
            query: (str) Search query
        Returns:
            (list) The results
        Raises:
            None
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
            data = ''
            raise CrawlRequestError('Request had code: {} and failed'.format(r.status_code))

        #  Convert the string from r.text to a python interpretable dict
        json_data = json.loads(data)
        
        # Extract the number of results form the data
        num_found = json_data['numFound']

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
            
            results.append(current_game)

        return results



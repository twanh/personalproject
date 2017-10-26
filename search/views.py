from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# App imports -- Import the databases
from games.models import Game, GameManager
from sellers.models import Seller

from webcrawler.crawlers import *

# Helper functions

def construct_game_detail_url(name, urls={}):
    ''' Create the url for the game (details) page '''

    # Create the primary key
    pk = Game.objects.all().order_by('-id')[0].pk + 1

    # Check if the kinguin url is given
    # If not find it!
    if 'kinguin' in urls:
        kinguin_url = urls['kinguin']
    else:
        # Search for the kinguin url
        king_search_results = Kinguin.search(name)
        if king_search_results is not None and len(king_search_results) > 0:
            kinguin_url = king_search_results[0]['url']
        else:
            kinguin_url = None

    # Check if the g2a url is given
    # If not, find it!
    if 'g2a' in urls:
        g2a_url = urls['g2a']
    else:
        # Search g2a url
        g2a_search_results = G2a.search(name)
        if g2a_search_results is not None and len(g2a_search_results) > 0:
            g2a_url = g2a_search_results[0]['url']
        else:
            g2a_url = None

    # Check if the gamestop url is given
    # If not, find it!
    if 'gamestop' in urls:
        gamestop_url = urls['gamestop']
    else:
        # Search gamestop url
        gamestop_search_results = Gamestop.search(name)
        if gamestop_search_results is not None and len(gamestop_search_results) > 0:
            gamestop_url = gamestop_search_results[0]['url']
        else:
            gamestop_url = None

    # Construct the final url
    # http://127.0.0.1:8000/games/15/?name=grand+theft+auto+v&g2a=https://www.g2a.com/grand-theft-auto-v-rockstar-key-global-i10000000788017&king=https://www.kinguin.net/category/15836/grand-theft-auto-v-rockstar-digital-download-key/&gamestop=http://www.gamestop.com/pc/games/grand-theft-auto-v/115461
    name = name.strip().replace(' ', '%20')
    if gamestop_url and gamestop_url[0] == '/':
        gamestop_url = 'https://gamestop.com{}'.format(gamestop_url)

    if g2a_url and kinguin_url and gamestop_url:
        url = '/games/{0}/?name={1}&g2a={2}&king={3}&gamestop={4}'.format(
            str(pk), name, g2a_url, kinguin_url, gamestop_url
        )
    elif g2a_url:
        if kinguin_url:
            url = '/games/{0}/?name={1}&g2a={2}&king={3}'.format(
                str(pk), name, g2a_url, kinguin_url
            )
        elif gamestop_url:
            url = '/games/{0}/?name={1}&g2a={2}&gamestop={3}'.format(
                str(pk), name, g2a_url, gamestop_url
            )
        else:
            url = '/games/{0}/?name={1}&g2a={2}'.format(
                str(pk), name, g2a_url
            )
    elif kinguin_url:
        if gamestop_url:
            url = '/games/{0}/?name={1}&king={2}&gamestop={3}'.format(
                str(pk), name, kinguin_url, gamestop_url
            )
        else:
            url = '/games/{0}/?name={1}&king={2}'.format(
                str(pk), name, kinguin_url
            )
    else:
        url = '/games/{0}/?name={1}&gamestop={2}'.format(
                str(pk), name, gamestop_url
            )

    return url


class ListSearch(generic.TemplateView):
    ''' Search a game, return to the game page '''
    
    #  Get the game title, etc...
    #  Check if the game exists in the current db
    #  Use some kind of smart search for the names etc...
    # If it does exist return to the game page
    # If there is not a exact match return all results
    #   And
    #   Crawl all the sellers for the game,
    #   Return all the results as search items

    def get(self, request):
        ''' Handles get request, and searches '''

        # Get the title the user searched for
        search_title = self.request.GET.get('title', '')
        
        force_more = self.request.GET.get('forceMore', 'false')

        search_status = 'Searching'
        # Check if the search title was given
        if search_title != '':

            # Gets all games from  db which contain the search_title
            games = Game.objects.all().filter(name__icontains=search_title)

            # Check if there are any results
            if len(games) > 0:
                # Set search results
                search_status = 'In database'
                db_results = games
                sellers_results = None

                if force_more != 'false':
                    sellers_results = []
                    search_status = 'Sellers'

                    # Do a search by the sellers
                    g2a_search = G2a.search(search_title)
                    kinguin_search = Kinguin.search(search_title)
                    gamestop_search = Gamestop.search(search_title)
                    
                    # print(type(g2a_search))

                    for results in g2a_search:
                        name = results['name']
                        price = results['price']
                        url = results['url']
                        local_url = construct_game_detail_url(name, urls={'g2a': url})
                        seller = 'G2a'
                        
                        sellers_results.append([name, price, url, seller, local_url])     

                    for results in kinguin_search:
                        name = results['name']                
                        price = results['price']
                        url = results['url']
                        local_url = construct_game_detail_url(name, urls={'kinguin': url})                    
                        seller = 'Kinguin'
                        sellers_results.append([name, price, url, seller, local_url])                    

                    for results in gamestop_search:
                        name = results['name']                
                        price = results['price']
                        if str(price).startswith('BUYDOWNLOAD$'):
                            price = price[12:]
                        url = results['url']
                        local_url = construct_game_detail_url(name, urls={'gamestop': url})                    
                        seller = 'Gamestop'
                        
                        sellers_results.append([name, price, url, seller, local_url])        

            else:
                db_results = None
                sellers_results = []
                search_status = 'Sellers'

                # Do a search by the sellers
                g2a_search = G2a.search(search_title)
                kinguin_search = Kinguin.search(search_title)
                gamestop_search = Gamestop.search(search_title)
                
                # print(type(g2a_search))

                for results in g2a_search:
                    name = results['name']
                    price = results['price']
                    url = results['url']
                    local_url = construct_game_detail_url(name, urls={'g2a': url})
                    seller = 'G2a'
                    
                    sellers_results.append([name, price, url, seller, local_url])     

                for results in kinguin_search:
                    name = results['name']                
                    price = results['price']
                    url = results['url']
                    local_url = construct_game_detail_url(name, urls={'kinguin': url})                    
                    seller = 'Kinguin'
                    sellers_results.append([name, price, url, seller, local_url])                    

                for results in gamestop_search:
                    name = results['name']                
                    price = results['price']
                    if str(price).startswith('BUYDOWNLOAD$'):
                        price = price[12:]
                    url = results['url']
                    local_url = construct_game_detail_url(name, urls={'gamestop': url})                    
                    seller = 'Gamestop'
                    
                    sellers_results.append([name, price, url, seller, local_url])        
                    
                # print(type(kinguin_search))
                # print(type(gamestop_search))

                # print(g2a_search, kinguin_search, gamestop_search)
        else:
            search_status = 'not in db'
            sellers_results = None
            db_results = None

        res = []

               

        print(res)

        context = {
            'status': search_status,
            'db': db_results,
            'sellers': sellers_results,
            'query': search_title
        }

        return render(request, 'search/search.html', context=context)

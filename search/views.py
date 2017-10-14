from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# App imports -- Import the databases
from games.models import Game, GameManager
from sellers.models import Seller

from webcrawler.crawlers import *

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
                    sellers_results.append([name, price, url])                    

                for results in kinguin_search:
                    name = results['name']                
                    price = results['price']
                    url = results['url']
                    sellers_results.append([name, price, url])                    

                for results in gamestop_search:
                    name = results['name']                
                    price = results['price']
                    url = results['url']
                    sellers_results.append([name, price, url])        
                    
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

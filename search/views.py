from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# App imports -- Import the databases
from games.models import Game, GameManager
from sellers.models import Seller


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

        search_title = self.request.GET.get('title', '')

        if search_title != '':
            # print( Game.objects.filter(
            #     name__icontains=search_title))
            
            games = Game.objects.all().filter(name__icontains=search_title)
            
            if games:
                print('not')
                print(games)
                # print(game.title)
                i = 0
                for game in games:
                    print(i)
                    print(game.name)
                    i+=1

                search_results = 'Found it'

            search_results = 'not in db'
            
        else:
            search_results = 'not in db'

        return HttpResponse(search_results)



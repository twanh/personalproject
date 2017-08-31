from django.shortcuts import redirect
from django.views import generic

from games.models import Game, GameManager
from webcrawler.crawlers import CrawlUrlError, CrawlNoResultsError


class GameView(generic.DetailView):
    ''' The view to show the games details page '''

    model = Game
    template_name = 'games/game.html'
    context_object_name = 'game'

    def get_object(self):
        ''' 
        Returns the object from the model
        If the object does not exist create a new one using the provided urls [GET] 
        and return those.
        '''

        # If the modal exists with the corresponding <pk> 
        # We return that object
        # If it does not exist a exception is raised
        # TODO: Find a way to only except the model does not exist exception.
        try:
            object = super(GameView, self).get_object()
        except Exception:

            # Get GET params from the request
            # And save the needed ones
            g2a_url = self.request.GET.get('g2a', '')
            kinguin_url = self.request.GET.get('king', '')
            # TODO: Add for other sites when crawler is done

            # Initialize the GameManager
            gm = GameManager()

            # Try to create add the new game.
            # If it fails we return a object of none. 
            # TODO: Find a better way to handle the CrawlUrlError. 
            # The CrawlURLError occurs when no valid url is provided.
            try:
                object =  gm._create_from_crawl(name=None, urls={'g2a': g2a_url, 'kinguin': kinguin_url})
            except CrawlUrlError:
                # return redirect('index')
                object = None

        return object
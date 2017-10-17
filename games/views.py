from django.shortcuts import redirect
from django.views import generic

from games.models import Game, GameManager
from webcrawler.crawlers import CrawlRequestError, CrawlUrlError, Reddit


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
            if not object.community_reddit:
                try:
                    reddit = Reddit.get_community_url(object.name)
                    object.community_reddit = reddit
                    object.save()
                except CrawlRequestError:
                    pass

        except Exception:
            # Get GET params from the request
            # And save the needed ones
            name = self.request.GET.get('name', None)
            g2a_url = self.request.GET.get('g2a', None)
            kinguin_url = self.request.GET.get('king', None)
            gamestop_url = self.request.GET.get('gamestop', None)
            
            if g2a_url is '' and kinguin_url is '' and gamestop_url is '':
                object = None

            # Initialize the GameManager
            gm = GameManager()

            # Try to create add the new game.
            # If it fails we return a object of none. 
            # TODO: Find a better way to handle the CrawlUrlError. 
            # The CrawlURLError occurs when no valid url is provided.
            if name is '':
                name = None
            try:
                
                
                # Check if king urls exists
                    # Check if g2a url exists
                        #  Check if gamestop url exists
                # Check if g2a url exits
                    # Check if gamestop url exists
                # Check if gamestop url exists
                if kinguin_url is not None:
                    if g2a_url is not None:
                        if gamestop_url is not None:
                            object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'kinguin': kinguin_url, 'gamestop': gamestop_url})
                        else:
                            object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'kinguin': kinguin_url})
                    else:
                        object = gm._create_from_crawl(name=name, urls={'kinguin': kinguin_url})
                elif g2a_url is not None:
                    if gamestop_url is not None:
                        object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'gamestop': gamestop_url})
                    else:
                        object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url})
                else:
                    object = gm._create_from_crawl(name=name, urls={'gamestop': gamestop_url})
                    
                # if g2a_url is not None and kinguin_url is not None and gamestop_url is not None:
                #     object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'kinguin': kinguin_url, 'gamestop': gamestop_url})
                # elif g2a_url is not None and kinguin_url is not None:
                #     object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'kinguin': kinguin_url})
                # elif kinguin_url is not None and gamestop_url is not None:
                #     object = gm._create_from_crawl(name=name, urls={'kinguin': kinguin_url, 'gamestop': gamestop_url})
                # elif gamestop_url is not None and g2a_url is not None:
                #     object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'gamestop': gamestop_url})
                # elif g2a
                # else:
                #     object = gm._create_from_crawl(name=name, urls={'g2a': g2a_url, 'kinguin': kinguin_url, 'gamestop': gamestop_url})

                    


            except CrawlUrlError:
                print('[CRAWL URL ERROR]')
                # return redirect('index')
                object = None

        return object
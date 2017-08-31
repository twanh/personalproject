from django.shortcuts import redirect
from django.views import generic

from games.models import Game, GameManager


class GameView(generic.DetailView):

    model = Game
    template_name = 'games/game.html'
    context_object_name = 'game'

    def get_object(self):
        try:
            object = super(GameView, self).get_object()
        except Exception as e:
            # Get GET params
            print(self.request.GET)
            # <QueryDict: {'g2a': ['https://g2a.com/h'], 'king': ['https://kinguin.com/h']}>

            g2a_url = self.request.GET.get('g2a', '')
            print(g2a_url)
            kinguin_url = self.request.GET.get('king', '')
            print(kinguin_url)
            # TODO: Add for other sites when crawler is done
            gm = GameManager()
            object =  gm._create_from_crawl(name=None, urls={'g2a': g2a_url, 'kinguin': kinguin_url})
            

        return object
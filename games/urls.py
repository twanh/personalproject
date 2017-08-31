from django.conf.urls import url

from games.views import GameView

urlpatterns = [

    # Show Game 
    # GameView - games:game-detail
    # /games/<pk>.
    url(r'^(?P<pk>\d+)/$', GameView.as_view(), name='game-detail')
]

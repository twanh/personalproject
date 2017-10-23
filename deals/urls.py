from django.conf.urls import url
from deals.views import *

urlpatterns = [
    
    # Full deals page
    # /deals/
    url(r'^$', AllDeals.as_view(), name='index'),

    # Details deal page
    # /deals/<pk>/
    url(r'^(?P<pk>\d+)/$', DetailDeal.as_view(), name='index')
]
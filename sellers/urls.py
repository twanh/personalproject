from django.conf.urls import url

from sellers.views import SellersListView

urlpatterns = [

    # Show All Sellers 
    # SellersListView - sellers:list
    # /sellers/
    url(r'^$', SellersListView.as_view(), name='list')
]

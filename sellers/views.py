from django.views import generic

from sellers.models import Seller

class SellersListView(generic.ListView):
    ''' Display all sellers with their rating and descriptions '''

    model = Seller
    template_name = 'sellers/list.html'
    context_object_name = 'sellers'
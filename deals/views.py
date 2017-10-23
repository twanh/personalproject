from django.shortcuts import render
from django.views.generic import ListView, DetailView

from deals.models import Deal

class AllDeals(ListView):
    ''' Display All Deals '''
    model = Deal
    template_name = 'deals/all.html'


class DetailDeal(DetailView):
    ''' Display one deal in detail '''
    model = Deal
    template_name = 'deals/detail.html'

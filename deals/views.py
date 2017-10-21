from django.shortcuts import render
from django.views.generic import ListView

from deals.models import Deal

class AllDeals(ListView):
    ''' Display All Deals '''
    model = Deal
    template_name = 'deals/all.html'

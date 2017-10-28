from django.shortcuts import render, reverse
from django.views.generic import ListView, TemplateView, FormView

from deals.models import Deal
from games.models import Game

from general import forms

class Index(ListView):
    model = Deal
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        # Get super
        context = super(Index, self).get_context_data(**kwargs)

        # Add context data
        context['index_header'] = Game.objects.get(pk=23)
        context['header_img'] = 'http://ll-c.ooyala.com/e1/FxZnluYjE6hEoFHu02TdwQqWA8tlkcwv/promo322349625'
        return context


class About(TemplateView):
    ''' Render the about page '''
    template_name = 'general/about.html'


class Contact(TemplateView):
    ''' Render contact page '''

    template_name = 'general/contact.html'
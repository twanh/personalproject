from django.shortcuts import get_object_or_404, reverse
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

from games.models import Game
from sellers.models import Seller

def proposal_email(request):

    print('rg', request.GET, len(request.GET))
    get_to          = request.GET.getlist('to')
    get_sender_name = request.GET.get('sender_name', '')
    get_game        = request.GET.get('game', '')    
    get_seller      = request.GET.get('seller', '')

    game    = get_object_or_404(Game, pk=get_game)
    seller  = get_object_or_404(Seller, pk=get_seller) 

    game_name       = game.name
    sender_name     = get_sender_name
    seller_name     = seller.name 
    seller_url      = seller.ref_url
    game_img        = game.image_url
    game_desc       = game.desc
    seller_desc     = seller.desc
    buy_url         = None
    original_price  = None
    price           = None
    game_url        = reverse('games:game-detail', kwargs={'pk': game.pk})

    if game.original_price == '0' or game.original_price is None:
        original_price = game.gamestop_price
    else:
        original_price = game.original_price
    
    if seller_name == 'G2a':
        buy_url = game.g2a_url
        price = game.g2a_price
    elif seller_name == 'Kinguin': 
        buy_url = game.get_kinguin_ref_url()
        price = game.kinguin_price
    elif seller_name == 'Gamestop':
        buy_url = game.gamestop_url
        price = game.gamestop_price
    else:
        buy_url = game.get_kinguin_ref_url()
        price = game.kinguin_price

    subject = 'A proposal from {}'.format(sender_name)
    to = get_to
    from_email = 'test@example.com'

    ctx = {
        'subject': 'A proposal from {}',
        'sender_name': get_sender_name,
        'game_name': game_name,
        'game_price': price,
        'seller': seller_name,
        'game_img': game_img,
        'game_desc': game_desc,
        'game_orig_price': original_price,
        'seller_home_url': seller_url,
        'seller_desc': seller_desc,
        'buy_url': buy_url,
        'game_url': 'https://domain.com/{}'.format(game_url)
    }

    message = get_template('sharing/emails/proposals/ProposalTemplate.html').render(ctx)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return HttpResponse('email_two')

from datetime import datetime

from django.db.models import F
from django.shortcuts import render
from django.views import View

from core.forms.user.forms import UserProfileForm
from core.models import Offers


def core(request):
    offers = Offers.objects.filter(is_published=True,
                                   dt_expiration__gte=datetime.now()).values(name=F('name_offer'),
                                                                             category_name=F('category__name'),
                                                                             offer_phone=F('phone'),
                                                                             offer_timework=F('time_work'),
                                                                             offer_avatar=F('author__profile__avatar'),
                                                                             offer_id=F('id')).order_by(
        'dt_updated')[:20]

    offers_vip = Offers.objects.filter(is_published=True,
                                       dt_expiration__gte=datetime.now(),
                                       type__ident='VIP').values(name=F('name_offer'),
                                                                 category_name=F('category__name'),
                                                                 offer_phone=F('phone'),
                                                                 offer_timework=F('time_work'),
                                                                 offer_avatar=F('author__profile__avatar'),
                                                                 offer_id=F('id')).order_by(
        'dt_updated')[:4]
    return render(request=request, template_name='main.html', context={
        "offers": offers,
        'offers_vip': offers_vip
    })


def solitaire(request):
    return render(request, 'games/solitaire.html', {})


def flappybird(request):
    return render(request, 'games/flappy.html', {})


def shooter(request):
    return render(request, 'games/shooter.html', {})

from django.db.models import F
from django.shortcuts import render

from core.models import Offers


def core(request):
    offers = Offers.objects.all().values(name=F('name_offer'), category_name=F('category__name'),
                                         offer_phone=F('phone'), offer_timework=F('time_work'),
                                         offer_avatar=F('author__profile__avatar'), offer_id=F('id')).order_by(
        'dt_updated')[:20]
    return render(request=request, template_name='main.html', context={
        "offers": offers
    })

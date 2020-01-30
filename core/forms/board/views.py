# in views.py
import json
from datetime import datetime, timedelta

from django.core import serializers
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.models import Offers, Regions, Category, Towns


def town_board(request, town):
    offers = Offers.objects.filter(town=town).values(name=F('name_offer'), category_name=F('category__name'),
                                                     offer_phone=F('phone'), offer_timework=F('time_work'),
                                                     offer_avatar=F('author__profile__avatar'),
                                                     offer_id=F('id')).order_by('-dt_updated')

    regions = Regions.objects.filter(id_town=town)
    categories = Category.objects.all()

    return render(request=request, template_name='board/town_board.html', context={
        "offers": offers,
        "town": town,
        'regions': regions,
        'categories': categories,
    })


def category_board(request, category):
    offers = Offers.objects.filter(category=category).values(name=F('name_offer'), category_name=F('category__name'),
                                                             offer_phone=F('phone'), offer_timework=F('time_work'),
                                                             offer_avatar=F('author__profile__avatar'),
                                                             offer_id=F('id')).order_by('-dt_updated')
    towns = Towns.objects.all()
    regions = Regions.objects.all()

    return render(request=request, template_name='board/category_board.html', context={
        "offers": offers,
        "towns": towns,
        'regions': regions,
        'category': category,
    })


def ajax_get_offers_body(request):
    town = request.POST.get('town')
    region = request.POST.get('region')
    category = request.POST.get('category')
    text_search = request.POST.get('text_search')
    page = request.POST.get('page')

    result = Offers.objects.filter(dt_expiration__gte=datetime.now(), is_published=True)
    if int(town) != 0:
        result = result.filter(town=town)
    if int(region) != 0:
        result = result.filter(region=region)
    if int(category) != 0:
        result = result.filter(category=category)
    if text_search:
        result = result.filter(name_offer__contains=text_search)

    result = result.values(name=F('name_offer'), category_name=F('category__name'),
                           offer_phone=F('phone'), offer_timework=F('time_work'),
                           offer_avatar=F('author__profile__avatar'),
                           offer_id=F('id')).order_by('-dt_updated')

    return HttpResponse(json.dumps(list(result)),
                        content_type='application/json')


def ajax_get_offers_url(request, town, region, category, page):
    if int(town) != 0 and int(region) == 0 and int(category) == 0:
        res = Offers.objects.filter(town=town,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')
    elif int(town) != 0 and int(region) != 0 and int(category) == 0:
        res = Offers.objects.filter(town=town, region=region,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')
    elif int(town) != 0 and int(region) == 0 and int(category) != 0:
        res = Offers.objects.filter(town=town, category=category,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')
    elif int(town) == 0 and int(region) == 0 and int(category) != 0:
        res = Offers.objects.filter(category=category,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')

    elif int(town) == 0 and int(region) != 0 and int(category) != 0:
        res = Offers.objects.filter(category=category, region=region,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')

    elif int(town) == 0 and int(region) == 0 and int(category) != 0:
        res = Offers.objects.filter(category=category,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')
    elif int(town) == 0 and int(region) == 0 and int(category) == 0:
        res = Offers.objects.filter(dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')

    else:
        res = Offers.objects.filter(town=town, region=region, category=category,
                                    dt_expiration__gte=datetime.now()).order_by(
            '-dt_updated')

    return res.values(name=F('name_offer'), category_name=F('category__name'),
                      offer_phone=F('phone'), offer_timework=F('time_work'),
                      offer_avatar=F('author__profile__avatar'),
                      offer_id=F('id')).order_by('-dt_updated')


def ajax_get_regions(request):
    town = request.POST.get('town')
    if town == 0:
        regions = Regions.objects.all()
    else:
        regions = Regions.objects.filter(id_town=town)
    return HttpResponse(serializers.serialize('json', regions),
                        content_type='application/json')


class TownOffersListJson(BaseDatatableView):
    model = Offers
    columns = ['offer_id', 'title', 'phone_number', 'nickname']
    order_columns = ['offer_id', 'title', 'phone_number', 'nickname']

    def filter_queryset(self, qs):
        town = self.request.GET.get('town')
        region = self.request.GET.get('region')
        category = self.request.GET.get('category')
        name = self.request.GET.get('name')
        result = Offers.objects.filter(town=town)

        if int(region) != 0:
            result = result.filter(region=region)

        if int(category) != 0:
            result = result.filter(category=category)

        if name is not None:
            result = result.filter(name_offer__contains=name)

        return result.values(offer_id=F('id'),
                             title=F('name_offer'),
                             phone_number=F('phone'),
                             nickname=F('author__profile__nickname'))
        #
        # return Offers.objects.filter(offer__town_id=town).values(review_id=F('id'),
        #                                                          town=F('offer__town__name'),
        #                                                          region=F('offer__region__name'),
        #                                                          offer_title=F('offer__name_offer'),
        #                                                          review_title=F('title'),
        #                                                          nickname=F('author__profile__nickname'),
        #                                                          time=F('dt_created'))

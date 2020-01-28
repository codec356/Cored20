# in views.py
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.forms.offer.forms import OffersForm, OfferCommentsForm, OfferReviewsForm, OfferReviewCommentsForm
from core.models import Offers, OfferComments, Regions, Category, OfferReviews, RateType, OfferReviewRates, \
    OfferReviewComments


@staff_member_required
def create_offer(request):
    if request.method == 'POST':
        form = OffersForm(data=request.POST,
                          initial={'author': request.user})

        if form.data['town'] == '' or form.data['region'] == '':
            form.add_error('region', 'Set town and region in profile')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Success')
                return redirect(reverse('core:main_page'))
            else:
                print('error')
                messages.error(request, 'Error')
                print(form.errors)
    else:
        form = OffersForm(initial={'author': request.user.id,
                                   'dt_created': datetime.utcnow(),
                                   # 'dt_expiration': datetime.utcnow() + timedelta(days=30)
                                   })
    return render(request, 'offer/create_offer.html', {'form': form})


def get_offer_iframe(request, offer):
    # offer = Offers.objects.get(pk=offer).values(name=F('name_offer'), offer_content=F('html_content'),
    #                                             offer_phone=F('phone'), offer_timework=F('time_work'),
    #                                             offer_review_id=F('id'))
    offer = Offers.objects.get(pk=offer)

    if request.user.is_authenticated:
        return render(request, 'offer/offer_iframe.html', context={
            "offer": offer
        })
    else:
        return redirect(reverse('core:login_url'))


def get_reviews_iframe(request, offer):
    reviews = []
    for review in OfferReviews.objects.filter(offer=offer).values('author__profile__nickname',
                                                                  'author__profile__avatar',
                                                                  'html_content',
                                                                  'id',
                                                                  'dt_created'):
        ratings = []
        for rating in OfferReviewRates.objects.filter(review_id=review['id']):
            ratings.append({
                'name': rating.rate_type.name,
                'n_rate': rating.n_rate
            })
        reviews.append({
            'id': review['id'],
            'author': review['author__profile__nickname'],
            'avatar': review['author__profile__avatar'],
            'content': review['html_content'],
            'dt_created': review['dt_created'],
            'ratings': ratings
        })
    if request.user.is_authenticated:
        return render(request=request, template_name='offer/reviews_iframe.html', context={
            'reviews': reviews
        })
    else:
        return redirect(reverse('core:login_url'))


def get_offer_page(request, offer):
    offer = Offers.objects.get(pk=offer)
    comments = OfferComments.objects.filter(offer=offer).values(avatar=F('author__profile__avatar'),
                                                                nickname=F('author__profile__nickname'),
                                                                author_id=F('author_id'),
                                                                time=F('dt_created'),
                                                                content=F('html_content'))
    return render(request=request, template_name='offer/offer_page.html', context={
        "offer": offer,
        "comments": comments,
        "form_comment": OfferCommentsForm(None, initial={
            'offer': offer,
            'author': request.user
        })
    })


def offer_comment(request):
    if request.POST:
        form = OfferCommentsForm(request=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))


def get_offer_reviews_board(request, town):
    regions = Regions.objects.filter(id_town=town)
    categories = Category.objects.all()

    context = {
        'regions': regions,
        'categories': categories,
        'town': town,
    }
    return render(request, 'offer/reviews_board.html', context)


class ReviewListJson(BaseDatatableView):
    model = OfferReviews
    columns = ['review_id', 'town', 'region', 'offer_title', 'review_title', 'nickname', 'time']
    order_columns = ['review_id', 'town', 'region', 'offer_title', 'review_title', 'nickname', 'time']

    def filter_queryset(self, qs):
        town = self.request.GET.get('town')
        region = self.request.GET.get('region')
        category = self.request.GET.get('category')
        if int(region) != 0 and int(category) != 0:

            return OfferReviews.objects.filter(offer__town=town,
                                               offer__region=region,
                                               offer__category=category).values(review_id=F('id'),
                                                                                town=F('offer__town__name'),
                                                                                region=F(
                                                                                    'offer__region__name'),
                                                                                offer_title=F('offer__name_offer'),
                                                                                review_title=F('title'),
                                                                                nickname=F('author__profile__nickname'),
                                                                                time=F('dt_created'))
        elif int(region) != 0 and int(category) == 0:

            return OfferReviews.objects.filter(offer__town=town,
                                               offer__region=region).values(review_id=F('id'),
                                                                            town=F('offer__town__name'),
                                                                            region=F('offer__region__name'),
                                                                            offer_title=F('offer__name_offer'),
                                                                            review_title=F('title'),
                                                                            nickname=F('author__profile__nickname'),
                                                                            time=F('dt_created'))
        elif int(region) == 0 and int(category) != 0:
            return OfferReviews.objects.filter(offer__town=town,
                                               offer__category=category).values(review_id=F('id'),
                                                                                town=F('offer__town__name'),
                                                                                region=F(
                                                                                    'offer__region__name'),
                                                                                offer_title=F('offer__name_offer'),
                                                                                review_review_title=F('title'),
                                                                                nickname=F('author__profile__nickname'),
                                                                                time=F('dt_created'))
        else:
            return OfferReviews.objects.filter(offer__town_id=town).values(review_id=F('id'),
                                                                           town=F('offer__town__name'),
                                                                           region=F('offer__region__name'),
                                                                           offer_title=F('offer__name_offer'),
                                                                           review_title=F('title'),
                                                                           nickname=F('author__profile__nickname'),
                                                                           time=F('dt_created'))


def offer_review(request):
    if request.method == 'POST':
        form = OfferReviewsForm(request=request.POST)
        if form.is_valid():
            if form.check_exists_review():
                return render(request, 'offer/error.html', {'error': '당신은 이미 이 제품에 관하여 검토를 남겨두었습니다'})
            review = form.save()
            for rate in RateType.objects.all():
                try:
                    n_rate = int(request.POST.get('rating_%s' % rate.id))
                except:
                    n_rate = 0
                form_rate = OfferReviewRates()
                form_rate.review = review
                form_rate.rate_type = rate
                form_rate.n_rate = n_rate
                form_rate.save()
            print(review)
            return redirect(reverse('core:page_review', kwargs={'review': review.pk}))
        else:
            messages.error(request, 'Error')
    else:
        form = OfferReviewsForm(None, initial={'author': request.user.id})
        return render(request, 'offer/create_review.html', {
            'form': form,
            'ratings': RateType.objects.all(),
        })


def get_review_page(request, review):
    review = OfferReviews.objects.get(pk=review)
    ratings = OfferReviewRates.objects.filter(review_id=review)

    comments = OfferReviewComments.objects.filter(review=review).values(avatar=F('author__profile__avatar'),
                                                                        nickname=F('author__profile__nickname'),
                                                                        author_id=F('author_id'),
                                                                        time=F('dt_created'),
                                                                        content=F('html_content'))

    form_comments = OfferReviewCommentsForm(None,
                                            initial={'author': request.user.id,
                                                     'review': review})
    return render(request=request, template_name='offer/review_page.html', context={
        "review": review,
        "ratings": ratings,
        "comments": comments,
        "form_comment": form_comments
    })


def review_comment(request):
    if request.POST:
        form = OfferReviewCommentsForm(request=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
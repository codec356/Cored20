# in views.py
import json

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.models import Offers


@user_passes_test(lambda u: u.is_superuser)
def admin_main(request):
    return render(request, 'admin_templates/base.html', {})


@user_passes_test(lambda u: u.is_superuser)
def users_table(request):
    return render(request, 'admin_templates/users/users.html', {})


class UsersView(BaseDatatableView):
    model = User
    columns = ['username', 'profile__nickname', 'balances__value', 'profile__level__n_level', 'is_staff',
               'profile__is_want_staff', 'profile__is_fake', 'id']
    order_columns = ['username', 'profile__nickname', 'balances__value', 'profile__level__n_level', 'is_staff',
                     'profile__is_want_staff', 'profile__is_fake', 'id']

    def filter_queryset(self, qs):
        username = self.request.GET.get('username')
        email = self.request.GET.get('email')
        is_staff = self.request.GET.get('is_staff')
        is_fake = self.request.GET.get('is_fake')
        is_want_staff = self.request.GET.get('is_want_staff')
        result = User.objects.filter()

        if username is not None:
            result = result.filter(username__contains=username)

        if email is not None:
            result = result.filter(email__contains=email)

        if is_staff is not None:
            result = result.filter(is_staff=is_staff)

        if is_fake is not None:
            result = result.filter(profile__is_fake=is_fake)

        if is_want_staff is not None:
            result = result.filter(profile__is_want_staff=is_want_staff)

        return result.values('username', 'profile__nickname', 'balances__value', 'profile__level__n_level', 'is_staff',
                             'profile__is_want_staff', 'profile__is_fake', 'id')


@user_passes_test(lambda u: u.is_superuser)
def change_user_staff_status(request):
    user_id = request.POST.get('user_id')
    if request.POST.get('is_staff') == 'true':
        is_staff = True
    else:
        is_staff = False
    user_obj = User.objects.get(id=user_id)
    user_obj.is_staff = is_staff
    user_obj.save()
    return json.dumps({
        'code': 200
    })


@user_passes_test(lambda u: u.is_superuser)
def offers_table(request):
    return render(request, 'admin_templates/offers/offers.html', {})


@user_passes_test(lambda u: u.is_superuser)
def offers_table_with_params(request, username):
    return render(request, 'admin_templates/offers/offers.html', {
        "username": username
    })


class OffersView(BaseDatatableView):
    model = User
    columns = ['author__username', 'author__profile__nickname', 'name_offer', 'is_published', 'dt_start',
               'dt_expiration', 'id']
    order_columns = ['author__username', 'author__profile__nickname', 'name_offer', 'is_published', 'dt_start',
                     'dt_expiration', 'id']

    def filter_queryset(self, qs):
        username = self.request.GET.get('username')
        result = Offers.objects.filter()

        if username is not None:
            result = result.filter(author__username__contains=username)
        return result.values('author__username', 'author__profile__nickname', 'name_offer', 'is_published', 'dt_start',
                             'dt_expiration', 'id')


@user_passes_test(lambda u: u.is_superuser)
def do_something_offer(request):
    action = request.POST.get('action')
    if action == 'publish':
        return publish_offer(request)
    if action == 'extend':
        return extend_offer(request)
    if action == 'delete':
        return delete_offer(request)


def publish_offer(request):
    offer_id = request.POST.get('offer_id')
    start = request.POST.get('start')
    end = request.POST.get('end')
    offer_obj = Offers.objects.get(pk=offer_id)
    offer_obj.dt_start = start
    offer_obj.dt_expiration = end
    offer_obj.is_published = True
    offer_obj.save()
    return HttpResponse(json.dumps({'code': 200}),
                        content_type='application/json')


def extend_offer(request):
    offer_id = request.POST.get('offer_id')
    end = request.POST.get('end')
    offer_obj = Offers.objects.get(pk=offer_id)
    offer_obj.dt_start = offer_obj.dt_start
    offer_obj.dt_expiration = end
    offer_obj.is_published = True
    offer_obj.save()
    return HttpResponse(json.dumps({'code': 200}),
                        content_type='application/json')


def delete_offer(request):
    offer_id = request.POST.get('offer_id')
    offer_obj = Offers.objects.get(pk=offer_id)
    offer_obj.is_published = False
    offer_obj.save()
    return HttpResponse(json.dumps({'code': 200}),
                        content_type='application/json')

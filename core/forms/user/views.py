# in views.py
import calendar
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, user_logged_in
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from core.forms.user.forms import UserForm, UserProfileForm, UserCreationForm
from core.models import BalanceMovements, TypesIncomes, Balances, Profile


def profile_view(request):
    if request.method == "POST":
        user = UserForm(data=request.POST, instance=request.user)
        try:
            profile = UserProfileForm(data=request.POST, instance=request.user.profile, files=request.FILES)
        except:
            profile = UserProfileForm(data=request.POST, files=request.FILES, initial={'experience': 0})

        if user.is_valid() and profile.is_valid():
            user = user.save()
            profile = profile.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(reverse('core:profile'))
        else:
            for rec in user.errors:
                messages.error(request, rec)
            for rec in profile.errors:
                messages.error(request, rec)
            messages.error(request=request, message='편집 중 오류')
            return render(request=request, context={
                "user_form": user,
                "profile_form": profile
            }, template_name='user/profile.html')
    else:
        user = UserForm(instance=request.user)
        try:
            profile = UserProfileForm(instance=request.user.profile)
        except:
            profile = UserProfileForm()
        return render(request=request, template_name='user/profile.html', context={
            "user_form": user,
            "profile_form": profile
        })


@receiver(user_logged_in)
def check_in(sender, user, request, **kwargs):
    dt = datetime.utcnow()
    if BalanceMovements.objects.filter(user=request.user.id,
                                       type_id=TypesIncomes.objects.get(action='Login').id,
                                       dt_income__gte=datetime(dt.year, dt.month, dt.day)).count() == 0:
        award_points(request.user, TypesIncomes.objects.get(action='Login'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def award_points(user, type_income, value=None):
    """
    Awards target the point value for key.  If key is an integer then it's a
    one off assignment and should be interpreted as the actual point value.
    """
    local_value = (value if value else type_income.value)
    apv = BalanceMovements(user=user, dt_income=datetime.now(), value=local_value, type=type_income)
    apv.save()
    usr_bal = Balances.objects.get(user=user)
    usr_bal.add_balance(local_value)
    usr_profile = Profile.objects.get(user=user)
    usr_profile.experience += local_value
    usr_profile.save()
    return usr_bal


def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.profile.level_id = 1
            # user.profile.is_want_staff = form.cleaned_data.get('is_want_staff')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.sex = form.cleaned_data.get('sex')

            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('core:main_page'))
    else:
        form = UserCreationForm()
    return render(request, 'user/registration.html', {'form': form})


def attendance_page(request):
    days_count = calendar.mdays[datetime.utcnow().month]
    return render(request=request, template_name='user/attendance.html', context={
        'days_count': days_count
    })


def attend(request):
    dt_cts = datetime.utcnow()
    if BalanceMovements.objects.filter(user=request.user.id,
                                       type_id=TypesIncomes.objects.get(action='attend').id,
                                       dt_income__gte=datetime(dt_cts.year, dt_cts.month, dt_cts.day)).count() == 0:
        award_points(request.user, TypesIncomes.objects.get(action='attend'))
        current_attend_count = BalanceMovements.objects.filter(type_id=TypesIncomes.objects.get(action='attend').id,
                                                               dt_income__gte=datetime(dt_cts.year, dt_cts.month,
                                                                                       dt_cts.day)).count()
        print(current_attend_count)
        if current_attend_count == 1:
            award_points(request.user, TypesIncomes.objects.get(action='first'))
        elif current_attend_count == 2:
            award_points(request.user, TypesIncomes.objects.get(action='second'))
        elif current_attend_count == 3:
            award_points(request.user, TypesIncomes.objects.get(action='third'))

        total_attend_count = BalanceMovements.objects.filter(user=request.user.id,
                                                             type_id=TypesIncomes.objects.get(
                                                                 action='attend').id).count()
        print(total_attend_count)

        if total_attend_count == 7:
            award_points(request.user, TypesIncomes.objects.get(action='seven_days'))
        elif total_attend_count == 30:
            award_points(request.user, TypesIncomes.objects.get(action='thirty_days'))
        elif total_attend_count == 365:
            award_points(request.user, TypesIncomes.objects.get(action='365_days'))
        elif total_attend_count == 500:
            award_points(request.user, TypesIncomes.objects.get(action='500_days'))
        elif total_attend_count == 730:
            award_points(request.user, TypesIncomes.objects.get(action='730_days'))
        elif total_attend_count == 1000:
            award_points(request.user, TypesIncomes.objects.get(action='1000_days'))
        else:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def count_attends(user):
    return BalanceMovements.objects.filter(user=user,
                                           type_id=TypesIncomes.objects.get(action='attend').id).count()

# in views.py
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.forms.resorts.forms import ResortCreationForm, ResortMessageCreationForm
from core.models import Resort, ResortMessages


def create_resort(request):
    if request.method == "POST":
        form = ResortCreationForm(request.POST, initial={
            'user': request.user
        })
        if form.is_valid():
            resort = form.save()
            return redirect(reverse('core:resort_page', kwargs={'resort': resort.id}))
    else:
        form = ResortCreationForm(initial={
            'user': request.user
        })
    return render(request, 'resorts/create_resort.html', {'form': form})


def resorts(request):
    return render(request=request, template_name='resorts/resorts_table.html', context={})


class ResortsListJson(BaseDatatableView):
    model = Resort
    columns = ['id', 'title', 'dt_created']
    order_columns = ['id', 'title', 'dt_created']

    def filter_queryset(self, qs):
        return Resort.objects.filter(solved=False, user=self.request.user)


def resort_page(request, resort):
    resort = Resort.objects.get(id=resort)
    if resort.user != request.user:
        return redirect('core:main_page')
    messages = ResortMessages.objects.filter(resort=resort).values(
        avatar=F('user__profile__avatar'),
        nickname=F('user__profile__nickname'),
        author_id=F('user_id'),
        time=F('dt_created'),
        html_content=F('content')
    )
    if request.method == 'POST':
        form_message = ResortMessageCreationForm(request.POST)
        if form_message.is_valid():
            form_message.save()
        else:
            return render(request=request, template_name='resorts/resort_page.html', context={
                'resort': resort,
                'messages': messages,
                'form_message': form_message
            })
    form_message = ResortMessageCreationForm(initial={
        'user': request.user,
        'resort': resort
    })
    return render(request=request, template_name='resorts/resort_page.html', context={
        'resort': resort,
        'messages': messages,
        'form_message': form_message
    })


def resort_message(request):
    if request.POST:
        form = ResortMessageCreationForm(request.POST)
        form.content = request.POST.get('content')
        form.resort = request.POST.get('resort')
        form.user = request.POST.get('user')
        print(form.content, form.resort, form.user)
        if form.is_valid():
            print('valid')
            form.save(commit=True)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(redirect_to=request.META.get('HTTP_REFERER'), content=request)

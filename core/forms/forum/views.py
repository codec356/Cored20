from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.forms.forum.forms import TopicForm, TopicCommentForm
from core.models import Topic, TopicComment


def topic(request, section):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic_obj = form.save()
            print('valid')
    else:
        form = TopicForm(None, initial={'user': request.user.id, 'section': section})
    return render(request, 'forum/create_topic.html', {
        'form': form,
    })


def topic_board(request, section):
    context = {
        'section': section,
    }
    return render(request, 'forum/forum.html', context)


class TopicListJson(BaseDatatableView):
    model = Topic
    columns = ['topic_id', 'topic_title', 'nickname', 'datetime', 'lookups']
    order_columns = ['topic_id', 'topic_title', 'nickname', 'datetime', 'lookups']

    def filter_queryset(self, qs):
        section = self.request.GET.get('section')
        return Topic.objects.filter(section=section).values(topic_id=F('id'),
                                                            topic_title=F('title'),
                                                            nickname=F('user__profile__nickname'),
                                                            datetime=F('dt_created'),
                                                            lookups=F('views'))


def topic_page(request, topic):
    topic_obj = Topic.objects.get(pk=topic)
    comments = TopicComment.objects.filter(topic_id=topic).values(avatar=F('user__profile__avatar'),
                                                                  nickname=F('user__profile__nickname'),
                                                                  user_id=F('user_id'),
                                                                  time=F('dt_created'),
                                                                  html_content=F('content'))
    context = {
        'topic': topic_obj,
        'comments': comments,
        'form_comment': TopicCommentForm(None,
                                         initial={'user': request.user.id,
                                                  'topic': topic_obj})
    }
    return render(request=request, template_name='forum/topic.html', context=context)


@transaction.atomic
def topic_comment(request):
    if request.method == 'POST':
        form = TopicCommentForm(request.POST)
        form.content = request.POST.get('content')
        form.topic = request.POST.get('topic')
        form.user = request.POST.get('user')
        form.dt_created = request.POST.get('dt_created')

        if form.is_valid():
            print(form.cleaned_data.values())
            form.save(commit=True)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print('errror')
            return redirect(request.META.get('HTTP_REFERER'))

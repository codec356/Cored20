from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse
from django_datatables_view.base_datatable_view import BaseDatatableView

from core.forms.resources.forms import ResourceTopicForm, ResourceTopicCommentForm
from core.models import ResourceTopic, ResourceTopicComment, SectionResource


def rs_topic(request, section_type):
    if request.method == 'POST':
        form = ResourceTopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic_obj = form.save()
            return redirect(reverse('core:rs_page_topic', kwargs={'topic': topic_obj.pk}))
    else:
        form = ResourceTopicForm(initial={'user': request.user.id, 'section_type': section_type})
    return render(request, 'resource_forum/create_topic.html', {
        'form': form,
    })


def rs_topic_board(request, section_type):
    context = {
        'section_type': section_type,
        'sections': SectionResource.objects.filter(type_id=section_type)
    }
    return render(request, 'resource_forum/forum.html', context)


class ResourceTopicListJson(BaseDatatableView):
    model = ResourceTopic
    columns = ['topic_id', 'preview_img', 'topic_title', 'nickname', 'datetime', 'lookups']
    order_columns = ['topic_id', 'preview_img', 'topic_title', 'nickname', 'datetime', 'lookups']

    def filter_queryset(self, qs):
        section_type = self.request.GET.get('section_type')
        section = self.request.GET.get('section')

        result = ResourceTopic.objects.filter(section__type__id=section_type)
        if int(section) != 0:
            result = result.filter(section=section)

        return result.values(topic_id=F('id'),
                             topic_title=F('title'),
                             preview_img=F('preview'),
                             nickname=F(
                                 'user__profile__nickname'),
                             datetime=F('dt_created'),
                             lookups=F('views'))


def rs_topic_page(request, topic):
    topic_obj = ResourceTopic.objects.get(pk=topic)
    topic_obj.views += 1
    topic_obj.save(update_fields=['views'])
    comments = ResourceTopicComment.objects.filter(topic_id=topic).values(avatar=F('user__profile__avatar'),
                                                                          nickname=F('user__profile__nickname'),
                                                                          user_id=F('user_id'),
                                                                          time=F('dt_created'),
                                                                          html_content=F('content'))
    context = {
        'topic': topic_obj,
        'comments': comments,
        'form_comment': ResourceTopicCommentForm(None,
                                                 initial={'user': request.user.id,
                                                          'topic': topic_obj})
    }
    return render(request=request, template_name='resource_forum/topic.html', context=context)


@transaction.atomic
def rs_topic_comment(request):
    if request.method == 'POST':
        form = ResourceTopicCommentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))

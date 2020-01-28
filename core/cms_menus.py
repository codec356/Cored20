from cms.menu_bases import CMSAttachMenu
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from core.models import Towns, Category, Section


class LocationMenu(CMSAttachMenu):
    name = _("Town menu")

    def get_nodes(self, request):
        nodes = []
        towns = Towns.objects.all().values('name', 'id')
        for town in towns:
            nodes.append(
                NavigationNode(town['name'], reverse("core:town_board", kwargs={'town': town['id']}), town['id']))
        return nodes


class ReviewsMenu(CMSAttachMenu):
    name = _("Reviews menu")

    def get_nodes(self, request):
        nodes = []
        towns = Towns.objects.all().values('name', 'id')
        for town in towns:
            nodes.append(
                NavigationNode(town['name'], reverse("core:table_reviews_board", kwargs={'town': town['id']}),
                               town['id']))
        return nodes


class CategoryMenu(CMSAttachMenu):
    name = _("Category menu")

    def get_nodes(self, request):
        nodes = []
        categories = Category.objects.all().values('name', 'id')
        for cat in categories:
            nodes.append(
                NavigationNode(cat['name'], reverse("core:category_board", kwargs={'category': cat['id']}), cat['id']))
        return nodes


class ForumMenu(CMSAttachMenu):
    name = _("Forum menu")

    def get_nodes(self, request):
        nodes = []

        if request.user.is_staff:
            sections = Section.objects.all()
        else:
            sections = Section.objects.filter(is_private=False)
        for sec in sections:
            nodes.append(NavigationNode(sec.title, reverse("core:table_topic_board", kwargs={'section': sec.id}),
                                        sec.title))
        return nodes


menu_pool.register_menu(LocationMenu)
menu_pool.register_menu(ReviewsMenu)
menu_pool.register_menu(CategoryMenu)
menu_pool.register_menu(ForumMenu)

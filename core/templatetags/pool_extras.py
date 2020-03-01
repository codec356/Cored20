from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Count, F
from django.template.loader_tags import register

from core.models import Towns, Category, Balances, Offers


@register.simple_tag(name='base_info')
def base_info(request):
    all_towns = Towns.objects.all().order_by('name')
    all_categories = Category.objects.all().order_by('name')
    # top_users = UserBalances.objects.values('level__n_level', 'user__nickname', 'user_id').annotate(user_count=Count('user')).order_by('-user_count')[:5]
    if request.user.is_authenticated:
        balances = {
            'value': Balances.objects.filter(user=request.user)[0].value
        }
    else:
        balances = ''

    offers_vip = Offers.objects.filter(is_published=True,
                                       dt_expiration__gte=datetime.now(),
                                       type__ident='VIP').values(name=F('name_offer'),
                                                                 category_name=F('category__name'),
                                                                 offer_phone=F('phone'),
                                                                 offer_timework=F('time_work'),
                                                                 offer_avatar=F('author__profile__avatar'),
                                                                 offer_id=F('id')).order_by(
        'dt_updated')[:4]

    return {
        'towns': all_towns,
        'categories': all_categories,
        # 'community': top_users,
        'balances': balances,
        'offers_vip': offers_vip
    }

# register.filter('base_info', base_info)
# @register.inclusion_tag('core/main.html')
# def get_towns(value):
#     all_towns = Towns.objects.all()
#
#     value = all_towns
#
#     return {'towns': value}
#
#
# register.filter('get_towns', get_towns)

from django.contrib.auth.models import User
from django.db.models import Count
from django.template.loader_tags import register

from core.models import Towns, Category, Balances


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

    return {
        'towns': all_towns,
        'categories': all_categories,
        # 'community': top_users,
        'balances': balances
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

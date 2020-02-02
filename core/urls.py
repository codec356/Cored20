from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from django.urls import path, include
from filebrowser.sites import site

from core import views
import core.forms.admin.views as admin_views
from core.forms.auction.views import auction_board
from core.forms.board.views import town_board, category_board, ajax_get_offers_url, \
    ajax_get_offers_body, ajax_get_regions, TownOffersListJson
from core.forms.forum.views import topic, topic_board, TopicListJson, topic_page, topic_comment
from core.forms.offer.views import create_offer, get_offer_iframe, get_reviews_iframe, get_offer_page, offer_comment, \
    get_offer_reviews_board, ReviewListJson, offer_review, get_review_page, review_comment
from core.forms.resorts.views import create_resort, ResortsListJson, resorts, resort_page, resort_message
from core.forms.user.forms import CustomLoginForm, logout_request
from core.forms.user.views import profile_view, check_in, create_user, attendance_page, attend

urlpatterns = [
    path('', views.core, name='main_page'),
    url(r'^profile/', profile_view, name='profile'),
    url(r'^filebrowser_filer/', include('ckeditor_filebrowser_filer.urls')),
    url(r'^admin/filebrowser/$', site.urls),
    url(r'^summernote/', include('django_summernote.urls')),
]

urlpatterns += [
    url(r'^create_offer/', create_offer, name='create_offer'),
    url(r'^edit_offer/', create_offer, name='edit_offer'),
    url(r'^iframe_offer=(?P<offer>[0-9]+)', get_offer_iframe, name='iframe_offer'),
    url(r'^iframe_reviews=(?P<offer>[0-9]+)', get_reviews_iframe, name='iframe_reviews'),
    url(r'^offer=(?P<offer>[0-9]+)', get_offer_page, name='page_offer'),
    url(r'^offer_comment/', offer_comment, name='offer_comment'),
    url(r'^trw_board=(?P<town>[0-9]+)', get_offer_reviews_board, name='table_reviews_board'),
    url(r'^datatable/reviews/$', ReviewListJson.as_view(), name='review_list_json'),
    url(r'^create_review/', offer_review, name='create_review'),
    url(r'^review=(?P<review>[0-9]+)', get_review_page, name='page_review'),
    url(r'^review_comment/', review_comment, name='review_comment'),

]

urlpatterns += [
    url(r'^registration/$', create_user, name='register_url'),
    url(r'^login/$', CustomLoginForm.as_view(), name="login_url"),
    url(r'^accounts/logout/$', logout_request, name='logout_url'),
    url(r'^profile/$', profile_view, name='profile'),
]

urlpatterns += [
    url(r'^tn_board=(?P<town>[0-9]+)/', town_board, name='town_board'),
    url(r'^datatable/towns/$', TownOffersListJson.as_view(), name='town_offers_list_json'),
    url(r'^tn=(?P<town>[0-9]+)&_rg=(?P<region>[0-9]+)&_cg=(?P<category>[0-9]+)&pg=(?P<page>[0-9]+)/',
        ajax_get_offers_url, name='ajax_get_offers_url'),
    url(r'^get_ajax_offers/', ajax_get_offers_body, name='ajax_get_offers_body'),
    url(r'^get_ajax_regions/', ajax_get_regions, name='ajax_get_regions'),
    url(r'^cg_board=(?P<category>[0-9]+)/', category_board, name='category_board'),
]

urlpatterns += [
    url(r'^section=(?P<section>[0-9]+)/create_topic/$', topic, name="create_topic"),
    url(r'^section=(?P<section>[0-9]+)$', topic_board, name='table_topic_board'),
    url(r'^datatable/topics/$', TopicListJson.as_view(), name='topic_list_json'),
    url(r'^topic=(?P<topic>[0-9]+)$', topic_page, name='page_topic'),
    url(r'^topic_comment/$', permission_required('is_authenticated')(topic_comment),
        name="topic_comment"),
]

urlpatterns += [
    url(r'^create_resort/$', create_resort, name="create_resort"),
    url(r'^resorts/$', resorts, name='resorts_table'),
    url(r'^datatable/resorts/$', ResortsListJson.as_view(), name='resort_list_json'),
    url(r'^resort=(?P<resort>[0-9]+)/$', resort_page, name="resort_page"),
    url(r'^resort_message/$', resort_message, name="resort_message"),
]

urlpatterns += [
    url(r'^attendance/$', attendance_page, name="attendance_page"),
    url(r'^attend/$', attend, name="attend"),
]

urlpatterns += [
    url(r'^auction/$', auction_board, name="auction_board"),
]

urlpatterns += [
    url(r'^adm/$', admin_views.admin_main, name='adm_main'),
    url(r'^adm/users/$', admin_views.users_table, name='adm_users_table'),
    url(r'^adm/datatable/users/$', admin_views.UsersView.as_view(), name='users_list_json'),
    url(r'^adm/users/actions/$', admin_views.change_user_staff_status, name='change_user_staff_status'),
    url(r'^adm/offers/$', admin_views.offers_table, name='adm_offers_table'),
    path('adm/offers=<str:username>/', admin_views.offers_table_with_params, name='adm_offers_table_username'),
    url(r'^adm/datatable/offers/$', admin_views.OffersView.as_view(), name='offers_list_json'),
    url(r'^adm/offers/actions/$', admin_views.do_something_offer, name='do_something_offer'),
]

from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django_select2.forms import ModelSelect2Widget
from django_summernote.widgets import SummernoteInplaceWidget

from core.models import Towns, Regions, Discounts, Offers, Category, OfferComments, OfferReviews, RateType, \
    OfferReviewRates, OfferReviewComments


class OffersForm(forms.ModelForm):
    name_offer = forms.CharField(max_length=100)
    phone = forms.CharField()
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=ModelSelect2Widget(
            model=Category,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0},
        )
    )
    town = forms.ModelChoiceField(
        queryset=Towns.objects.all(),
        widget=ModelSelect2Widget(
            model=Towns,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0},
        )
    )

    region = forms.ModelChoiceField(
        queryset=Regions.objects.all(),
        widget=ModelSelect2Widget(
            model=Regions,
            search_fields=['name__icontains'],
            dependent_fields={'town': 'id_town'},
            max_results=500,
            attrs={'data-minimum-input-length': 0},
        )
    )

    discount = forms.ModelChoiceField(
        queryset=Discounts.objects.all(),
        widget=ModelSelect2Widget(
            model=Discounts,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0},
        ),
        required=False
    )
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    is_new = forms.BooleanField(required=False)
    dt_expiration = forms.DateTimeField(widget=forms.HiddenInput())
    dt_updated = forms.DateTimeField(widget=forms.HiddenInput())
    dt_created = forms.DateTimeField(widget=forms.HiddenInput())
    html_content = forms.CharField(widget=SummernoteInplaceWidget())
    time_work = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(OffersForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = kwargs.get('author')
        self.fields['dt_updated'].initial = datetime.utcnow()

    class Meta:
        model = Offers
        fields = '__all__'
        widgets = {'name_offer': forms.HiddenInput(),
                   'html_content': SummernoteInplaceWidget(attrs={
                       'summernote':
                           {
                               'width': '800',
                           }})}


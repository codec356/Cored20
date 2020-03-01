from datetime import datetime

from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
from django import forms
from django.contrib.auth.models import User
from django.forms import SplitDateTimeWidget, SelectDateWidget, DateTimeInput
from django_select2.forms import ModelSelect2Widget
from django_summernote.widgets import SummernoteInplaceWidget

from core.models import Offers, Auction


class AuctionCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    # offer = forms.ModelChoiceField(
    #     queryset=Offers.objects.filter(is_published=True),
    #     label=u"Offer",
    #     widget=ModelSelect2Widget(
    #         model=Offers,
    #         search_fields=['name_offer__icontains'],
    #         max_results=500,
    #         dependent_fields={
    #             'user': 'author'
    #         },
    #         attrs={'data-minimum-input-length': 0},
    #     ),
    #     required=False
    # )

    title = forms.CharField(max_length=20)
    # description = forms.CharField(max_length=4096, widget=SummernoteInplaceWidget(), required=False)
    start_price = forms.IntegerField(required=True)
    current_price = forms.IntegerField(required=False)

    dt_expiration = forms.DateTimeField(widget=DateTimePickerInput(), required=True, label='종료일')
    secret_key = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AuctionCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Auction
        fields = '__all__'

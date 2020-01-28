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


class OfferCommentsForm(forms.ModelForm):
    offer = forms.ModelChoiceField(queryset=Offers.objects.all(), widget=forms.HiddenInput)
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    html_content = forms.CharField(widget=SummernoteInplaceWidget(attrs={
        'summernote':
            {
                'width': '100%',
                'toolbar': [
                    ['style', ['style']],
                    ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript', 'strikethrough', 'clear']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['height', ['height']],
                    ['insert', ['link']],
                    ['view', ['fullscreen']],
                ]
            }}))
    dt_created = forms.DateTimeField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        super(OfferCommentsForm, self).__init__(data=request, *args, **kwargs)
        self.fields['dt_created'].initial = datetime.now()

    class Meta:
        model = OfferComments
        fields = '__all__'
        widgets = {'name_offer': forms.HiddenInput(),
                   'html_content': SummernoteInplaceWidget()}


# class OfferReviewsForm(forms.ModelForm):
#     offer = forms.ModelChoiceField(queryset=Offers.objects.all(), widget=forms.HiddenInput())
#     user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
#     title = forms.CharField(max_length=128, widget=forms.HiddenInput(), required=False)
#     html_content = forms.CharField(max_length=4096, widget=SummernoteInplaceWidget())
#     dt_created = forms.DateTimeField(widget=forms.HiddenInput())
#
#     def __init__(self, request, *args, **kwargs):
#         super(OfferReviewsForm, self).__init__(data=request, *args, **kwargs)
#         self.fields['dt_created'].initial = datetime.now()
#
#     class Meta:
#         model = OfferReviews
#         fields = '__all__'

class OfferReviewsForm(forms.ModelForm):
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
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label=u"Category",
        widget=ModelSelect2Widget(
            model=Regions,
            search_fields=['name__icontains'],
            max_results=500,
            attrs={'data-minimum-input-length': 0},
        )
    )
    offer = forms.ModelChoiceField(
        queryset=Offers.objects.all(),
        label=u"Offer",
        widget=ModelSelect2Widget(
            model=Offers,
            search_fields=['name_offer__icontains'],
            dependent_fields={
                'town': 'town',
                'region': 'region',
                'category': 'category'},
            max_results=500,
            attrs={'data-minimum-input-length': 0},
        )
    )

    title = forms.CharField(max_length=20)
    html_content = forms.CharField(max_length=4096, widget=SummernoteInplaceWidget())
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        super(OfferReviewsForm, self).__init__(data=request, *args, **kwargs)

    class Meta:
        model = OfferReviews
        fields = '__all__'

    def check_exists_review(self):
        if OfferReviews.objects.filter(author=self.cleaned_data['author'],
                                       offer=self.cleaned_data['offer']).count() > 0:
            return True
        else:
            return False


class OfferReviewRatesForm(forms.ModelForm):
    review = forms.ModelChoiceField(queryset=OfferReviews.objects.all(), widget=forms.HiddenInput)
    rate_type = forms.ModelChoiceField(queryset=RateType.objects.all(), widget=forms.HiddenInput)
    n_rate = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = OfferReviewRates
        fields = '__all__'


class OfferReviewCommentsForm(forms.ModelForm):
    review = forms.ModelChoiceField(queryset=OfferReviews.objects.all(), widget=forms.HiddenInput)
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    html_content = forms.CharField(widget=SummernoteInplaceWidget(attrs={
        'summernote':
            {
                'toolbar': [
                    ['style', ['style']],
                    ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript', 'strikethrough', 'clear']],
                    ['fontsize', ['fontsize']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['height', ['height']],
                    ['insert', ['link']],
                    ['view', ['fullscreen']],
                ]
            }}))
    dt_created = forms.DateTimeField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        super(OfferReviewCommentsForm, self).__init__(data=request, *args, **kwargs)
        self.fields['dt_created'].initial = datetime.now()

    class Meta:
        model = OfferReviewComments
        fields = '__all__'
        widgets = {'html_content': SummernoteInplaceWidget()}

from datetime import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django_select2.forms import ModelSelect2Widget
from django_summernote.widgets import SummernoteInplaceWidget

from core.models import ResortType, Resort, ResortMessages


class ResortCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    type = forms.ModelChoiceField(
        queryset=ResortType.objects.all(),
        widget=ModelSelect2Widget(
            model=ResortType,
            search_fields=['name__icontains'],
            attrs={'data-minimum-input-length': 0},
        ),
        required=True
    )
    title = forms.CharField(max_length=128, required=True)
    content = forms.CharField(widget=SummernoteInplaceWidget(attrs={
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
            }}), required=True)

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'validate'}, api_params={'hl': 'ko'}))

    class Meta:
        model = Resort
        fields = '__all__'
        widgets = {'user': forms.HiddenInput(),
                   'content': SummernoteInplaceWidget()}

    def __init__(self, *args, **kwargs):
        super(ResortCreationForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = kwargs.get('user')

    def save(self, commit=True):
        resort = Resort.objects.create(
            user=self.cleaned_data['user'],
            type=self.cleaned_data['type'],
            title=self.cleaned_data['title'],
            dt_created=datetime.utcnow()
        )
        resort.save()
        resort_message = ResortMessages.objects.create(
            resort=resort,
            user=self.cleaned_data['user'],
            content=self.cleaned_data['content'],
            dt_created=datetime.utcnow()
        )
        resort_message.save()
        return resort


class ResortMessageCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    resort = forms.ModelChoiceField(queryset=Resort.objects.all(), widget=forms.HiddenInput())
    content = forms.CharField(widget=SummernoteInplaceWidget(attrs={
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
            }}), required=True)

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'validate'}, api_params={'hl': 'ko'}))

    class Meta:
        model = ResortMessages
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ResortMessageCreationForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = kwargs.get('user')
        self.fields['resort'].initial = kwargs.get('resort')




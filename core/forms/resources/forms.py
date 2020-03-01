from datetime import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.files.images import get_image_dimensions
from django_select2.forms import ModelSelect2Widget
from django_summernote.widgets import SummernoteInplaceWidget

from core.models import User, Section, Topic, TopicComment, ResourceTopicComment, ResourceTopic, SectionResource, \
    SectionResourceType


class SectionResourceForm(forms.ModelForm):
    title = forms.CharField(max_length=150)

    class Meta:
        model = Section
        fields = '__all__'


class ResourceTopicForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
    preview = forms.ImageField(required=False)
    title = forms.CharField(max_length=150)
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
            }}))
    section_type = forms.ModelChoiceField(queryset=SectionResourceType.objects.all(), widget=forms.HiddenInput)
    section = forms.ModelChoiceField(
        queryset=SectionResource.objects.filter(),
        label=u"Section",
        widget=ModelSelect2Widget(
            model=SectionResource,
            search_fields=['name_offer__icontains'],
            max_results=500,
            dependent_fields={
                'section_type': 'type'
            },
            attrs={'data-minimum-input-length': 0},
        ),
        required=False
    )

    def clean_preview(self):
        preview = self.cleaned_data['preview']
        if preview:
            try:
                w, h = get_image_dimensions(preview)

                main, sub = preview.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(_('Please use a JPEG, '
                                                  'GIF or PNG image.'))

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new preview
                """
                pass

        return preview

    def __init__(self, *args, **kwargs):
        super(ResourceTopicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ResourceTopic
        fields = '__all__'


class ResourceTopicCommentForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
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
            }}))
    topic = forms.ModelChoiceField(queryset=ResourceTopic.objects.all(), widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ResourceTopicCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ResourceTopicComment
        fields = '__all__'

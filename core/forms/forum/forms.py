from datetime import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget

from core.models import User, Section, Topic, TopicComment


class SectionForm(forms.ModelForm):
    title = forms.CharField(max_length=150)

    class Meta:
        model = Section
        fields = '__all__'


class TopicForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
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
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Topic
        fields = '__all__'


class TopicCommentForm(forms.ModelForm):
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
    dt_created = forms.DateTimeField(widget=forms.HiddenInput)
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(TopicCommentForm, self).__init__(*args, **kwargs)
        self.fields['dt_created'].initial = datetime.now()

    class Meta:
        model = TopicComment
        fields = '__all__'

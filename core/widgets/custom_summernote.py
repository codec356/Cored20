import json
from distutils.command.config import config

from django import forms
from django.conf import settings as django_settings
from django.templatetags.static import static
from django.forms.utils import flatatt
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_summernote.utils import get_proper_language, using_config, \
    has_codemirror_config
from django_summernote.widgets import SummernoteWidgetBase, SummernoteInplaceWidget


@using_config
class SummernoteInplaceWidgetOffer(SummernoteWidgetBase):
    @using_config
    def summernote_settings(self):
        lang = get_proper_language()

        summernote_settings = config.get('summernote', {}).copy()
        summernote_settings.update({
            'lang': lang,
            'url': {
                'language': static('summernote/lang/summernote-' + lang + '.min.js'),
                'upload_attachment': reverse('django_summernote-upload_attachment'),
            },
        })
        return summernote_settings
    @using_config
    def _media(self):
        return forms.Media(
            css={
                'all': (
                        (config['codemirror_css'] if has_codemirror_config() else ()) +
                        config['default_css'] +
                        config['css_for_inplace']
                )
            },
            js=(
                    (config['codemirror_js'] if has_codemirror_config() else ()) +
                    config['default_js'] +
                    config['js_for_inplace']
            ))

    media = property(_media)

    @using_config
    def render(self, name, value, attrs=None, **kwargs):
        summernote_settings = self.summernote_settings()
        summernote_settings.update(self.attrs.get('summernote', {}))

        html = super(SummernoteInplaceWidgetOffer, self).render(
            name, value, attrs=attrs, **kwargs
        )
        config['toolbar'] = [
            # ['style', ['style']],
            ['view', ['fullscreen', 'codeview']],
            ['help', ['help']],
        ]

        context = {
            'id': attrs['id'],
            'id_safe': attrs['id'].replace('-', '_'),
            'attrs': self.final_attr(attrs),
            'config': config,
            'settings': json.dumps(summernote_settings),
            'CSRF_COOKIE_NAME': django_settings.CSRF_COOKIE_NAME,
        }

        html += render_to_string('django_summernote/widget_inplace.html', context)
        return mark_safe(html)

    def final_attr(self, attr):
        attrs_for_final = super(SummernoteInplaceWidgetOffer, self).final_attr(attr)
        # crispy form render bug
        if 'class' in attrs_for_final:
            attrs_for_final['class'] = attrs_for_final['class'].replace(' form-control', '')
        return attrs_for_final



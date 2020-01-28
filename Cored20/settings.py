import os  # isort:skip
from django.utils.translation import ugettext as _

from core.utils import my_custom_upload_to_func

gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for Cored20 project.

Generated by 'django-admin startproject' using Django 1.11.27.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!sji*p+0hc!bo0=c6l5f)4-^#2ayjk2w44*zr!9vp%scxm3ih^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', "renew.opi1.com", "opi1.com", "www.opi1.com"]

# Application definition


ROOT_URLCONF = 'Cored20.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/plugins/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'plugins')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static', 'custom'),
    os.path.join(BASE_DIR, 'static', 'custom', 'lib'),
)
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Cored20', 'templates'), os.path.join(BASE_DIR, 'Cored20',
                                                                              'templates/admin_templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_file',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'Cored20',
    'core',
    'djangocms_icon',
    'bootstrap3',
    'django_select2',
    'mathfilters',
    'django_cleanup.apps.CleanupConfig',
    'django_summernote',
    'bootstrap3_datepicker',
    'captcha',
]

LANGUAGES = (
    ## Customize this
    ('en-us', gettext('en')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'code': 'en-us',
            'redirect_on_fallback': True,
            'public': True,
            'name': gettext('English'),
            'hide_untranslated': False,
        },
    ],
    'default': {
        'hide_untranslated': False,
        'redirect_on_fallback': True,
        'public': True,
    },
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right')
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'core_cms',
        'USER': 'django',
        'PASSWORD': 'db',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'opicom_20',
#         'USER': 'opicom_dj',
#         'PASSWORD': 'django_db',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

MIGRATION_MODULES = {

}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

DATA_UPLOAD_MAX_MEMORY_SIZE = 5428800

SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    # 'width': 800,
    'height': '250',
    # Use proper language setting automatically (default)
    # 'lang': None,

    # Or, set editor language/locale forcely
    'lang': 'ko-KR',

    # Customize toolbar buttons
    'toolbar': [
        # ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript', 'strikethrough', 'clear']],
        # ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        # ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video', 'hr']],
        ['view', ['fullscreen', 'codeview']],
        ['help', ['help']],
    ],

    # Need authentication while uploading attachments.
    'attachment_require_authentication': True,

    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func,
    'attachment_filesize_limit': 50000000,
    # Set custom storage class for attachments.
    # 'attachment_storage_class': 'my.custom.storage.class.name',

    # Set custom model for attachments (default: 'django_summernote.Attachment')
    # 'attachment_model': 'my.custom.attachment.model', # must inherit 'django_summernote.AbstractAttachment'

    # Set common css/js media files
    'base_css': (
        # '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
    ),
    'base_js': (
        # '//code.jquery.com/jquery-1.9.1.min.js',
        # '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
    'default_css': (
        os.path.join(STATIC_URL, 'summernote/summernote.css'),
        os.path.join(STATIC_URL, 'summernote/django_summernote.css'),
    ),
    'default_js': (
        os.path.join(STATIC_URL, 'summernote/jquery.ui.widget.js'),
        os.path.join(STATIC_URL, 'summernote/jquery.iframe-transport.js'),
        os.path.join(STATIC_URL, 'summernote/jquery.fileupload.js'),
        os.path.join(STATIC_URL, 'summernote/summernote.min.js'),
    ),

    # You can disable file upload feature.
    'disable_upload': False,

    # Codemirror as codeview
    # If any codemirror settings are defined, it will include codemirror files automatically.
    'css': {
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    },
    'codemirror': {
        'mode': 'htmlmixed',
        'lineNumbers': 'true',

        # You have to include theme file in 'css' or 'css_for_inplace' before using it.
        'theme': 'monokai',
    },

    # Lazy initialize
    # If you want to initialize summernote at the bottom of page, set this as True
    # and call `initSummernote()` on your page.
    'lazy': True,

    # To use external plugins,
    # Include them within `css` and `js`.
    # 'js': {
    #     '/some_static_folder/summernote-ext-print.js',
    #     '//somewhere_in_internet/summernote-plugin-name.js',
    # },
    # You can also add custom settings in `summernote` section.
    # 'summernote': {
    #     'print': {
    #         'stylesheetUrl': '/some_static_folder/printable.css',
    #     },
    # }
}

RECAPTCHA_PUBLIC_KEY = '6LfFHMgUAAAAAF_Z70shQhnJrRbO-ELOV-VPwg1S'
RECAPTCHA_PRIVATE_KEY = '6LfFHMgUAAAAAPLWSqXduwD2ZNXzUzsbzrxEOE-u'

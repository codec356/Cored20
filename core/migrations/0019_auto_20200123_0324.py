# Generated by Django 2.0 on 2020-01-23 00:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0018_auto_20200123_0258'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OfferReviewsComments',
            new_name='OfferReviewComments',
        ),
        migrations.RenameModel(
            old_name='OfferReviewsRates',
            new_name='OfferReviewRates',
        ),
    ]
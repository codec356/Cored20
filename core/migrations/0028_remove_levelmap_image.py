# Generated by Django 2.0 on 2020-03-13 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200313_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='levelmap',
            name='image',
        ),
    ]
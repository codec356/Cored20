# Generated by Django 2.0 on 2020-01-24 18:21

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20200124_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='html_content',
            field=tinymce.models.HTMLField(),
        ),
    ]

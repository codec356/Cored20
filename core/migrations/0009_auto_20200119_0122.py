# Generated by Django 2.0 on 2020-01-18 22:22

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200118_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='html_content',
            field=tinymce.models.HTMLField(),
        ),
    ]

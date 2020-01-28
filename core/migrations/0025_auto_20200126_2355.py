# Generated by Django 2.0 on 2020-01-26 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200124_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='dt_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='offers',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='offers',
            name='dt_expiration',
            field=models.DateTimeField(null=True),
        ),
    ]

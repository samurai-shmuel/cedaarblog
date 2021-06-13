# Generated by Django 3.2.3 on 2021-06-07 11:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210607_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='author_str',
            field=models.CharField(default='Anonymous', max_length=150),
        ),
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blogpost', to=settings.AUTH_USER_MODEL),
        ),
    ]

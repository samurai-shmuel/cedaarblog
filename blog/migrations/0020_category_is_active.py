# Generated by Django 3.2.3 on 2021-06-21 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_user_is_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

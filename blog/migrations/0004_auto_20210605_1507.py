# Generated by Django 3.2.3 on 2021-06-05 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_posts_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]

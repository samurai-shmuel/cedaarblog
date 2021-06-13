# Generated by Django 3.2.3 on 2021-06-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_posts_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='category',
        ),
        migrations.AddField(
            model_name='posts',
            name='category',
            field=models.ManyToManyField(related_name='related_posts', to='blog.Category'),
        ),
    ]

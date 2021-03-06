# Generated by Django 3.2.3 on 2021-06-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20210612_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_posts', to='blog.Category'),
        ),
    ]

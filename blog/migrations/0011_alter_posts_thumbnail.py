# Generated by Django 3.2.3 on 2021-06-09 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210607_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]

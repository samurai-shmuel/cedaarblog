# Generated by Django 3.2.3 on 2021-06-07 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_posts_thumbnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='user_id',
            new_name='commenter',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='post_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.posts'),
        ),
    ]

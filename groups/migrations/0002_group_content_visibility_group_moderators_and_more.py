# Generated by Django 4.2.6 on 2023-11-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_visibility'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='content_visibility',
            field=models.IntegerField(choices=[(1, 'Visible to everyone'), (2, 'Visible to registered users'), (3, 'Visible to group members')], default=1),
        ),
        migrations.AddField(
            model_name='group',
            name='moderators',
            field=models.ManyToManyField(related_name='moderators', to='users.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='requested_for_moderator',
            field=models.ManyToManyField(related_name='requested_for_moderator', to='users.profile'),
        ),
    ]
# Generated by Django 4.2.6 on 2023-11-24 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='visibility',
            field=models.IntegerField(choices=[(1, 'Visible to everyone'), (2, 'Visible to registered users'), (3, 'Visible to group members')], default=1),
        ),
    ]
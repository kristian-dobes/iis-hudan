# Generated by Django 4.2.6 on 2023-10-15 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("username", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=255)),
                ("profile_picture_url", models.CharField(max_length=200)),
                ("bio", models.CharField(max_length=1024)),
            ],
        ),
    ]
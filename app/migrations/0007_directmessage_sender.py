# Generated by Django 4.2.dev20220919031901 on 2022-12-01 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0006_alter_channel_people_alter_directmessage_both_people"),
    ]

    operations = [
        migrations.AddField(
            model_name="directmessage",
            name="sender",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

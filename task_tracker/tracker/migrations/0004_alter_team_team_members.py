# Generated by Django 4.0.5 on 2022-06-25 18:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0003_alter_team_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="team_members",
            field=models.ManyToManyField(
                related_name="teams", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-26 06:15

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0004_alter_team_team_members"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="team_members",
        ),
        migrations.AddField(
            model_name="task",
            name="task_memebers",
            field=models.ManyToManyField(
                related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="completed_at",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="task",
            name="started_at",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="task",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tracker.team"
            ),
        ),
    ]

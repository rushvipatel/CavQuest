# Generated by Django 4.2.6 on 2023-10-19 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CavQuest_app", "0002_usersubmission"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="approved_status",
            field=models.BooleanField(default=False),
        ),
    ]

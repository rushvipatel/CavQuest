# Generated by Django 4.2 on 2023-11-12 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CavQuest_app", "0023_alter_adminsubmission_facts_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="image",
            field=models.ImageField(null=True, upload_to="location_images/"),
        ),
    ]

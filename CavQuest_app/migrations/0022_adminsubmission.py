# Generated by Django 4.2 on 2023-11-12 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CavQuest_app", "0021_usertask"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminSubmission",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                            ("denied", "Denied"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "difficulties",
                    models.CharField(
                        choices=[
                            ("easy", "EASY"),
                            ("medium", "MEDIUM"),
                            ("hard", "HARD"),
                        ],
                        default="easy",
                        max_length=10,
                    ),
                ),
                ("task_text", models.CharField(max_length=200, null=True)),
                ("hint1", models.CharField(max_length=200, null=True)),
                ("hint2", models.CharField(max_length=200, null=True)),
                ("hint3", models.CharField(max_length=200, null=True)),
                ("description", models.CharField(max_length=200, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="staticfiles/location_images"
                    ),
                ),
                ("facts", models.TextField(blank=True, max_length=100000, null=True)),
                ("approved", models.BooleanField(default=True)),
            ],
        ),
    ]

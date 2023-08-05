# Generated by Django 2.2.3 on 2019-08-23 22:00

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IndexStats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "stats",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        encoder=django.core.serializers.json.DjangoJSONEncoder
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TableStats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "stats",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        encoder=django.core.serializers.json.DjangoJSONEncoder
                    ),
                ),
            ],
        ),
    ]

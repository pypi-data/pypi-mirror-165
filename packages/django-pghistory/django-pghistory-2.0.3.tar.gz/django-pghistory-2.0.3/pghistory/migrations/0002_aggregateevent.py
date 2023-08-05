# Generated by Django 3.0.7 on 2020-06-23 14:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("pghistory", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="AggregateEvent",
            fields=[
                (
                    "pgh_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("pgh_created_at", models.DateTimeField(auto_now_add=True)),
                ("pgh_label", models.TextField(help_text="The event label.")),
                (
                    "pgh_table",
                    models.CharField(
                        help_text="The table under which the event is stored",
                        max_length=64,
                    ),
                ),
                (
                    "pgh_data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        help_text="The raw data of the event row"
                    ),
                ),
                (
                    "pgh_diff",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        help_text="The diff between the previous event and the current event"
                    ),
                ),
            ],
            options={"managed": False},
        )
    ]

# Generated by Django 4.2.3 on 2023-07-27 11:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("topic", "0002_initial_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="grade",
            name="publish_date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
    ]

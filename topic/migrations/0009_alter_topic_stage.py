# Generated by Django 4.2.3 on 2023-09-12 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
        ('topic', '0008_remove_stage_teacher_remove_your_stage_stage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.stage'),
        ),
    ]
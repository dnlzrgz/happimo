# Generated by Django 5.0.6 on 2024-05-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("moods", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="activity",
            options={"ordering": ["name"], "verbose_name_plural": "activities"},
        ),
        migrations.AlterModelOptions(
            name="entry",
            options={"ordering": ["-date", "-time"], "verbose_name_plural": "entries"},
        ),
        migrations.AlterModelOptions(
            name="mood",
            options={"ordering": ["-name"]},
        ),
        migrations.RemoveField(
            model_name="mood",
            name="icon",
        ),
        migrations.AddField(
            model_name="mood",
            name="color",
            field=models.CharField(default="#000", max_length=7),
        ),
        migrations.AlterField(
            model_name="mood",
            name="name",
            field=models.CharField(max_length=20),
        ),
    ]

# Generated by Django 4.2.9 on 2024-03-31 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NotesApp", "0005_alter_notes_file_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Remainder",
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
                ("time", models.DateTimeField()),
                ("note", models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name="notes",
            name="file_type",
            field=models.CharField(
                choices=[
                    ("IMG", "IMAGE"),
                    ("TXT", "TEXT"),
                    ("PDF", "PDF"),
                    ("VID", "VIDEO"),
                    ("DEF", "DEFAULT"),
                ],
                default="DEF",
                max_length=10,
            ),
        ),
    ]
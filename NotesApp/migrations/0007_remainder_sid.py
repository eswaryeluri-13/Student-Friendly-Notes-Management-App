# Generated by Django 4.2.9 on 2024-03-31 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("NotesApp", "0006_remainder_alter_notes_file_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="remainder",
            name="sid",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
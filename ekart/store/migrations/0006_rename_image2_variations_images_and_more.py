# Generated by Django 4.1.4 on 2023-05-09 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_variations"),
    ]

    operations = [
        migrations.RenameField(
            model_name="variations",
            old_name="image2",
            new_name="images",
        ),
        migrations.RemoveField(
            model_name="variations",
            name="image3",
        ),
        migrations.RemoveField(
            model_name="variations",
            name="image4",
        ),
    ]
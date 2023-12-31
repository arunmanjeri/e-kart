# Generated by Django 4.1.4 on 2023-05-09 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0007_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Cancelled", "Cancelled"),
                    ("Accepted", "Accepted"),
                    ("New", "New"),
                    ("Completed", "Completed"),
                ],
                default="New",
                max_length=10,
            ),
        ),
    ]

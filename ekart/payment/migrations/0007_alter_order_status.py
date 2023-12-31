# Generated by Django 4.1.4 on 2023-05-08 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0006_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Completed", "Completed"),
                    ("New", "New"),
                    ("Accepted", "Accepted"),
                    ("Cancelled", "Cancelled"),
                ],
                default="New",
                max_length=10,
            ),
        ),
    ]

# Generated by Django 4.1.4 on 2023-05-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0008_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Completed", "Completed"),
                    ("Cancelled", "Cancelled"),
                    ("New", "New"),
                    ("Accepted", "Accepted"),
                ],
                default="New",
                max_length=10,
            ),
        ),
    ]

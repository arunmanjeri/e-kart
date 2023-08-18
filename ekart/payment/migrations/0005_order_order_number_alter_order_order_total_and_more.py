# Generated by Django 4.1.4 on 2023-05-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0004_remove_order_order_number_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="order_number",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_total",
            field=models.FloatField(),
        ),
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
        migrations.AlterField(
            model_name="order",
            name="tax",
            field=models.FloatField(),
        ),
    ]

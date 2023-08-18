# Generated by Django 4.1.4 on 2023-05-01 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category_color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_color", models.CharField(max_length=20)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category_size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_size", models.CharField(max_length=20)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category_type",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_type", models.CharField(max_length=20)),
                ("is_active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=200, unique=True)),
                ("description", models.TextField(blank=True, max_length=500)),
                ("price", models.IntegerField()),
                ("images", models.ImageField(blank=True, upload_to="photos/products")),
                ("stock", models.IntegerField()),
                ("is_available", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("modified_date", models.DateTimeField(auto_now=True)),
                (
                    "category_color",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.category_color",
                    ),
                ),
                (
                    "category_size",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.category_size",
                    ),
                ),
                (
                    "category_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.category_type",
                    ),
                ),
            ],
        ),
    ]
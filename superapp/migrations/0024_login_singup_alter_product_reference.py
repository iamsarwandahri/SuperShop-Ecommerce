# Generated by Django 4.1 on 2024-01-04 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("superapp", "0023_alter_product_desc_alter_product_reference"),
    ]

    operations = [
        migrations.CreateModel(
            name="Login",
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
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Singup",
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
                ("username", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("password", models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name="product",
            name="reference",
            field=models.CharField(default="9095dec4", max_length=100),
        ),
    ]
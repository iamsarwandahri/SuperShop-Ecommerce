# Generated by Django 4.1 on 2024-01-11 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("superapp", "0025_delete_login_delete_singup_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="reference",
            field=models.CharField(default="81283606", max_length=100),
        ),
    ]
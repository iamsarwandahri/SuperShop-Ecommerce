# Generated by Django 4.1 on 2023-12-24 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superapp', '0013_countries_alter_product_reference_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='reference',
            field=models.CharField(default='54f912ce', max_length=100),
        ),
    ]
# Generated by Django 4.1 on 2023-12-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superapp', '0004_order_update_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reference',
            field=models.CharField(default='<function Product.generate_unique_code at 0x00000254183EA700>', max_length=100),
        ),
    ]

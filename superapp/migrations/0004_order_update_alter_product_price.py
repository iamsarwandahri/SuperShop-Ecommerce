# Generated by Django 4.1 on 2023-12-19 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superapp', '0003_customer_order_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='update',
            field=models.CharField(default='Order Pending!', max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
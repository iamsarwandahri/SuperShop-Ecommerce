# Generated by Django 4.1 on 2023-12-30 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superapp', '0021_alter_checkout_comments_alter_product_reference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='cashonDelivery',
            new_name='cashOnDelivery',
        ),
        migrations.AlterField(
            model_name='product',
            name='reference',
            field=models.CharField(default='0f2ae0a2', max_length=100),
        ),
    ]

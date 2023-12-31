# Generated by Django 4.1 on 2023-12-29 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superapp', '0016_alter_product_price_alter_product_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('MAN', 'MAN'), ('WOMAN', 'WOMAN'), ('KIDS', 'KIDS'), ('OTHER', 'OTHER')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='reference',
            field=models.CharField(default='23451a5a', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=models.CharField(choices=[('Footwear', 'Footwear'), ('Clothes', 'Clothes'), ('Accessories', 'Accessories'), ('Clearance', 'Clearance'), ('Technology', 'Technology'), ('Sports', 'Sports'), ('Toy', 'Toy')], max_length=50),
        ),
    ]

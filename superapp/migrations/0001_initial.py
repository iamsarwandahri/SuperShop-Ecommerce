# Generated by Django 4.1 on 2023-12-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('p_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=264)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('new', models.BooleanField(default=False)),
                ('sale', models.BooleanField(default=False)),
                ('category', models.CharField(choices=[(1, 'Footwear'), (2, 'Clothes'), (3, 'Accessories'), (4, 'Clearance')], max_length=50)),
                ('sub_category', models.CharField(choices=[(1, 'MAN'), (2, 'WOMAN'), (3, 'KIDS')], max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='product_images')),
            ],
        ),
    ]
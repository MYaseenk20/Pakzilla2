# Generated by Django 3.0.3 on 2020-09-07 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Customer'),
        ),
    ]

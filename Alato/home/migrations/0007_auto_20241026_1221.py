# Generated by Django 3.2.25 on 2024-10-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_order_arrival_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='home.CartItem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

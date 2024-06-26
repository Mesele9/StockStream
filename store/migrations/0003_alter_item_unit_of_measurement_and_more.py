# Generated by Django 4.2.13 on 2024-06-14 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_supplier_issuerecord_voucher_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='unit_of_measurement',
            field=models.CharField(choices=[('Piece', 'Piece'), ('Kilogram', 'Kilogram'), ('Gram', 'Gram'), ('Liter', 'Liter'), ('Milliliter', 'Milliliter'), ('Bottle', 'Bottle'), ('Crate', 'Crate'), ('Pack', 'Pack'), ('Box', 'Box'), ('Bag', 'Bag'), ('Dozen', 'Dozen'), ('Meter', 'Meter'), ('Centimeter', 'Centimeter'), ('Square Meter', 'Square Meter'), ('Cubic Meter', 'Cubic Meter')], max_length=50),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=250),
        ),
    ]

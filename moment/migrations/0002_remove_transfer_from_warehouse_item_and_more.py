# Generated by Django 5.1 on 2024-10-16 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfer',
            name='from_warehouse_item',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='to_warehouse_item',
        ),
    ]

# Generated by Django 5.1 on 2024-09-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_bookreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='rating',
            field=models.PositiveIntegerField(verbose_name=(1, 2, 3, 4)),
        ),
    ]

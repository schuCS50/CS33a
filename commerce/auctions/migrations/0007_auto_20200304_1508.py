# Generated by Django 3.0.3 on 2020-03-04 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200302_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlistitem',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

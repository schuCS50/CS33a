# Generated by Django 3.0.3 on 2020-03-03 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing_watchlistitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing'),
            preserve_default=False,
        ),
    ]

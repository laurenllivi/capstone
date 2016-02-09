# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0015_listing_price_per_hour_weekend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price_per_hour',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='listing',
            name='price_per_hour_weekend',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=0, blank=True),
            preserve_default=True,
        ),
    ]

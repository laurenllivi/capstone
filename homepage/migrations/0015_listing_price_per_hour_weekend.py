# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0014_auto_20160208_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price_per_hour_weekend',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]

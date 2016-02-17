# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_auto_20160210_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='listing',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
            preserve_default=True,
        ),
    ]

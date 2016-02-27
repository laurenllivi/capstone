# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20160225_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='currently_listed',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_auto_20160216_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='longitude',
        ),
        migrations.AddField(
            model_name='listing',
            name='geolocation',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]

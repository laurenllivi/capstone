# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_auto_20160206_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='listing',
            field=models.ForeignKey(default=1, to='homepage.Listing'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20160225_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing_photo',
            name='listing',
            field=models.ForeignKey(default=1, to='homepage.Listing'),
            preserve_default=False,
        ),
    ]

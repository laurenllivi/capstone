# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing_photo',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, to='homepage.Listing'),
            preserve_default=True,
        ),
    ]

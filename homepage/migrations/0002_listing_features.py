# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='features',
            field=models.ManyToManyField(to='homepage.Feature'),
            preserve_default=True,
        ),
    ]

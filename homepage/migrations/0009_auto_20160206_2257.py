# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_auto_20160206_2252'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Document',
            new_name='Image',
        ),
    ]

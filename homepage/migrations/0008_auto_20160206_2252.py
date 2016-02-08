# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_auto_20160206_2240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='file_name',
            new_name='image_name',
        ),
        migrations.RemoveField(
            model_name='document',
            name='docfile',
        ),
        migrations.AddField(
            model_name='document',
            name='image_file',
            field=models.ImageField(default=datetime.datetime(2016, 2, 6, 22, 52, 51, 856988, tzinfo=utc), upload_to=b'venue-images'),
            preserve_default=False,
        ),
    ]

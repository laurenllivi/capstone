# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_auto_20160206_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(default=b'venue-images/None/no-img.jpg', upload_to=b'venue-images'),
            preserve_default=True,
        ),
    ]

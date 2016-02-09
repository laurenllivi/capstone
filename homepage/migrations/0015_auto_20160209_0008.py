# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0014_auto_20160208_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(default='venue-images/None/no-img.jpg', upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='listing_photo',
            name='image_file',
            field=models.ImageField(default='venue-images/None/no-img.jpg', upload_to=''),
            preserve_default=True,
        ),
    ]

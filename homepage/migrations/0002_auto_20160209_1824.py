# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to='', default='venue-images/None/no-img.jpg'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='listing_photo',
            name='image_file',
            field=models.ImageField(upload_to='', default='venue-images/None/no-img.jpg'),
            preserve_default=True,
        ),
    ]

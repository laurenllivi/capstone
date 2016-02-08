# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_auto_20160208_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing_photo',
            name='alt_title',
        ),
        migrations.RemoveField(
            model_name='listing_photo',
            name='name',
        ),
        migrations.AddField(
            model_name='listing_photo',
            name='image_file',
            field=models.ImageField(default=b'venue-images/None/no-img.jpg', upload_to=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='listing_photo',
            name='image_name',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='listing_photo',
            name='image_title',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]

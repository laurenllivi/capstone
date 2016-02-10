# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_remove_listing_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_photo',
            name='alt_title',
        ),
        migrations.RemoveField(
            model_name='user_photo',
            name='name',
        ),
        migrations.AddField(
            model_name='user_photo',
            name='image_file',
            field=models.ImageField(default='profile-images/no-img.jpg', upload_to=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user_photo',
            name='image_name',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user_photo',
            name='image_title',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
    ]

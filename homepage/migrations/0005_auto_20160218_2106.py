# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_auto_20160210_0201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing_date',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='listing_date',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='listing_date',
            name='status',
        ),
        migrations.AddField(
            model_name='listing',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 2, 18, 21, 6, 16, 574977, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 18, 21, 6, 27, 934520, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing_date',
            name='date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rental_request',
            name='request_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 18, 21, 6, 33, 958675, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 18, 21, 6, 37, 462001, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(null=True, auto_now_add=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20160129_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing_Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('alt_title', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('alt_title', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='photo',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='user',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ForeignKey(null=True, blank=True, to='homepage.User_Photo'),
            preserve_default=True,
        ),
    ]

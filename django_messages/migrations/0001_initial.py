# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('subject', models.CharField(max_length=120, verbose_name='Subject')),
                ('body', models.TextField(verbose_name='Body')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='sent at')),
                ('read_at', models.DateTimeField(blank=True, null=True, verbose_name='read at')),
                ('read', models.NullBooleanField(default=False)),
                ('replied_at', models.DateTimeField(blank=True, null=True, verbose_name='replied at')),
                ('sender_deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Sender deleted at')),
                ('recipient_deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Recipient deleted at')),
                ('parent_msg', models.ForeignKey(related_name='next_messages', to='django_messages.Message', blank=True, null=True, verbose_name='Parent message')),
                ('recipient', models.ForeignKey(related_name='received_messages', to=settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name='Recipient')),
                ('sender', models.ForeignKey(related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name_plural': 'Messages',
                'verbose_name': 'Message',
                'ordering': ['-sent_at'],
            },
        ),
    ]

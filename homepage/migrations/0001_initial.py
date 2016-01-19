# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', max_length=30, unique=True)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(blank=True, null=True, max_length=15)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Add_On',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('item_name', models.CharField(blank=True, null=True, max_length=255)),
                ('description', models.CharField(blank=True, null=True, max_length=500)),
                ('quantity_available', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=8)),
                ('price_per', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('address_type', models.CharField(blank=True, null=True, max_length=255)),
                ('street', models.CharField(blank=True, null=True, max_length=255)),
                ('street2', models.CharField(blank=True, null=True, max_length=255)),
                ('city', models.CharField(blank=True, null=True, max_length=255)),
                ('state', models.CharField(blank=True, null=True, max_length=255)),
                ('zipcode', models.CharField(blank=True, null=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
                ('description', models.CharField(blank=True, null=True, max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, null=True, max_length=255)),
                ('category', models.CharField(blank=True, null=True, max_length=255)),
                ('price_per_hour', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=8)),
                ('listing_type', models.CharField(blank=True, null=True, max_length=255)),
                ('description', models.CharField(blank=True, null=True, max_length=500)),
                ('sq_footage', models.IntegerField(blank=True, null=True)),
                ('num_guests', models.IntegerField(blank=True, null=True)),
                ('parking_desc', models.CharField(blank=True, null=True, max_length=255)),
                ('address', models.ForeignKey(to='homepage.Address')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Date',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.NullBooleanField(default=False)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('feature', models.ForeignKey(to='homepage.Feature')),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(blank=True, null=True, max_length=255)),
                ('body', models.CharField(blank=True, null=True, max_length=255)),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_recipient')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_sender')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('alt_title', models.CharField(blank=True, null=True, max_length=255)),
                ('name', models.CharField(blank=True, null=True, max_length=255)),
                ('listing', models.ForeignKey(blank=True, to='homepage.Listing', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recovery_String',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('rand_string', models.CharField(blank=True, null=True, max_length=255)),
                ('expiration', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rental_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('notes', models.CharField(blank=True, null=True, max_length=255)),
                ('approved', models.NullBooleanField(default=False)),
                ('listing_date', models.ForeignKey(to='homepage.Listing_Date')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, null=True, max_length=500)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=8)),
                ('paid', models.NullBooleanField(default=False)),
                ('notes', models.CharField(blank=True, null=True, max_length=255)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='transaction_owner')),
                ('rental_request', models.ForeignKey(to='homepage.Rental_Request')),
                ('renter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='transaction_renter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='add_on',
            name='listing',
            field=models.ForeignKey(to='homepage.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ForeignKey(to='homepage.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.Group', verbose_name='groups', related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='user permissions', related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.'),
            preserve_default=True,
        ),
    ]

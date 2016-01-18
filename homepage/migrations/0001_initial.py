# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=15, blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Add_On',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('item_name', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('quantity_available', models.CharField(max_length=255, blank=True, null=True)),
                ('price_per', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('address_type', models.CharField(max_length=255, blank=True, null=True)),
                ('street', models.CharField(max_length=255, blank=True, null=True)),
                ('street2', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255, blank=True, null=True)),
                ('state', models.CharField(max_length=255, blank=True, null=True)),
                ('zipcode', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('category', models.CharField(max_length=255, blank=True, null=True)),
                ('price_per_hour', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)),
                ('listing_type', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('sq_footage', models.IntegerField(blank=True, null=True)),
                ('num_guests', models.IntegerField(blank=True, null=True)),
                ('parking_desc', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('time_stamp', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=255, blank=True, null=True)),
                ('body', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('alt_title', models.CharField(max_length=255, blank=True, null=True)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('listing', models.ForeignKey(to='homepage.Listing', blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recovery_String',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rand_string', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('notes', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)),
                ('paid', models.NullBooleanField(default=False)),
                ('notes', models.CharField(max_length=255, blank=True, null=True)),
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
            field=models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_name='user_set', related_query_name='user', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', blank=True, related_name='user_set', related_query_name='user', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]

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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Add_On',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('quantity_available', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('price_per', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=50, null=True, blank=True)),
                ('image_title', models.CharField(max_length=20, null=True, blank=True)),
                ('image_file', models.ImageField(default=b'venue-images/None/no-img.jpg', upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('category', models.CharField(max_length=255, null=True, blank=True)),
                ('price_per_hour', models.DecimalField(null=True, max_digits=8, decimal_places=0, blank=True)),
                ('price_per_hour_weekend', models.DecimalField(null=True, max_digits=8, decimal_places=0, blank=True)),
                ('listing_type', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('sq_footage', models.IntegerField(null=True, blank=True)),
                ('num_guests', models.IntegerField(null=True, blank=True)),
                ('parking_desc', models.CharField(max_length=255, null=True, blank=True)),
                ('street', models.CharField(max_length=255, null=True, blank=True)),
                ('street2', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(max_length=255, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=255, null=True, blank=True)),
                ('features', models.ManyToManyField(to='homepage.Feature')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Date',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature', models.ForeignKey(to='homepage.Feature')),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=50, null=True, blank=True)),
                ('image_title', models.CharField(max_length=20, null=True, blank=True)),
                ('image_file', models.ImageField(default=b'venue-images/None/no-img.jpg', upload_to=b'')),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField(null=True, blank=True)),
                ('subject', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.CharField(max_length=255, null=True, blank=True)),
                ('recipient', models.ForeignKey(related_name='message_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recovery_String',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rand_string', models.CharField(max_length=255, null=True, blank=True)),
                ('expiration', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rental_Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(max_length=255, null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('price', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('paid', models.NullBooleanField(default=False)),
                ('notes', models.CharField(max_length=255, null=True, blank=True)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
                ('owner', models.ForeignKey(related_name='transaction_owner', to=settings.AUTH_USER_MODEL)),
                ('rental_request', models.ForeignKey(to='homepage.Rental_Request')),
                ('renter', models.ForeignKey(related_name='transaction_renter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alt_title', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='image',
            name='listing',
            field=models.ForeignKey(to='homepage.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='add_on',
            name='listing',
            field=models.ForeignKey(to='homepage.Listing'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ForeignKey(blank=True, to='homepage.User_Photo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]

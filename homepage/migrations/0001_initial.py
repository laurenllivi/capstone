# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=15, blank=True, null=True)),
                ('groups', models.ManyToManyField(related_name='user_set', verbose_name='groups', to='auth.Group', blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=500, blank=True, null=True)),
                ('quantity_available', models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=2)),
                ('price_per', models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=500, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image_name', models.CharField(max_length=50, blank=True, null=True)),
                ('image_title', models.CharField(max_length=20, blank=True, null=True)),
                ('image_file', models.ImageField(upload_to='', default='venue-images/None/no-img.jpg')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('category', models.CharField(max_length=255, blank=True, null=True)),
                ('price_per_hour', models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=0)),
                ('price_per_hour_weekend', models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=0)),
                ('listing_type', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=500, blank=True, null=True)),
                ('sq_footage', models.IntegerField(blank=True, null=True)),
                ('num_guests', models.IntegerField(blank=True, null=True)),
                ('parking_desc', models.CharField(max_length=255, blank=True, null=True)),
                ('street', models.CharField(max_length=255, blank=True, null=True)),
                ('street2', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255, blank=True, null=True)),
                ('state', models.CharField(max_length=255, blank=True, null=True)),
                ('zipcode', models.CharField(max_length=255, blank=True, null=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('geolocation', django.contrib.gis.db.models.fields.PointField(srid=4326, blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Date',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image_name', models.CharField(max_length=50, blank=True, null=True)),
                ('image_title', models.CharField(max_length=20, blank=True, null=True)),
                ('image_file', models.ImageField(upload_to='', default='venue-images/None/no-img.jpg')),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=255, blank=True, null=True)),
                ('body', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('notes', models.CharField(max_length=255, blank=True, null=True)),
                ('approved', models.NullBooleanField(default=False)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(max_length=500, blank=True, null=True)),
                ('review_date', models.DateTimeField(auto_now_add=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('price', models.DecimalField(max_digits=8, blank=True, null=True, decimal_places=2)),
                ('paid', models.NullBooleanField(default=False)),
                ('notes', models.CharField(max_length=255, blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('image_name', models.CharField(max_length=50, blank=True, null=True)),
                ('image_title', models.CharField(max_length=50, blank=True, null=True)),
                ('image_file', models.ImageField(upload_to='', default='profile-images/no-img.jpg')),
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
            field=models.ForeignKey(null=True, to='homepage.User_Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', verbose_name='user permissions', to='auth.Permission', blank=True, related_query_name='user', help_text='Specific permissions for this user.'),
            preserve_default=True,
        ),
    ]

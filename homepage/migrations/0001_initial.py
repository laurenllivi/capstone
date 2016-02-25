# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=75, blank=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('phone', models.CharField(null=True, max_length=15, blank=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_query_name='user', blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(null=True, max_length=255, blank=True)),
                ('description', models.CharField(null=True, max_length=500, blank=True)),
                ('quantity_available', models.DecimalField(max_digits=8, null=True, decimal_places=2, blank=True)),
                ('price_per', models.DecimalField(max_digits=8, null=True, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(null=True, max_length=255, blank=True)),
                ('description', models.CharField(null=True, max_length=500, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(null=True, max_length=50, blank=True)),
                ('image_title', models.CharField(null=True, max_length=20, blank=True)),
                ('image_file', models.ImageField(default='venue-images/None/no-img.jpg', upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(null=True, max_length=255, blank=True)),
                ('category', models.CharField(null=True, max_length=255, blank=True)),
                ('price_per_hour', models.DecimalField(max_digits=8, null=True, decimal_places=0, blank=True)),
                ('price_per_hour_weekend', models.DecimalField(max_digits=8, null=True, decimal_places=0, blank=True)),
                ('listing_type', models.CharField(null=True, max_length=255, blank=True)),
                ('description', models.CharField(null=True, max_length=500, blank=True)),
                ('sq_footage', models.IntegerField(null=True, blank=True)),
                ('num_guests', models.IntegerField(null=True, blank=True)),
                ('parking_desc', models.CharField(null=True, max_length=255, blank=True)),
                ('street', models.CharField(null=True, max_length=255, blank=True)),
                ('street2', models.CharField(null=True, max_length=255, blank=True)),
                ('city', models.CharField(null=True, max_length=255, blank=True)),
                ('state', models.CharField(null=True, max_length=255, blank=True)),
                ('zipcode', models.CharField(null=True, max_length=255, blank=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('geolocation', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True, blank=True)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing_Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(null=True, max_length=50, blank=True)),
                ('image_title', models.CharField(null=True, max_length=20, blank=True)),
                ('image_file', models.ImageField(default='venue-images/None/no-img.jpg', upload_to='')),
                ('listing', models.ForeignKey(to='homepage.Listing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(null=True, blank=True)),
                ('subject', models.CharField(null=True, max_length=255, blank=True)),
                ('body', models.CharField(null=True, max_length=255, blank=True)),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_recipient')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='message_sender')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recovery_String',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rand_string', models.CharField(null=True, max_length=255, blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(null=True, max_length=255, blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(null=True, blank=True)),
                ('description', models.CharField(null=True, max_length=500, blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True, auto_now_add=True)),
                ('price', models.DecimalField(max_digits=8, null=True, decimal_places=2, blank=True)),
                ('paid', models.NullBooleanField(default=False)),
                ('notes', models.CharField(null=True, max_length=255, blank=True)),
                ('listing', models.ForeignKey(to='homepage.Listing')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='transaction_owner')),
                ('rental_request', models.ForeignKey(to='homepage.Rental_Request')),
                ('renter', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='transaction_renter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(null=True, max_length=50, blank=True)),
                ('image_title', models.CharField(null=True, max_length=50, blank=True)),
                ('image_file', models.ImageField(default='profile-images/no-img.jpg', upload_to='')),
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
            field=models.ManyToManyField(verbose_name='user permissions', related_query_name='user', blank=True, related_name='user_set', help_text='Specific permissions for this user.', to='auth.Permission'),
            preserve_default=True,
        ),
    ]

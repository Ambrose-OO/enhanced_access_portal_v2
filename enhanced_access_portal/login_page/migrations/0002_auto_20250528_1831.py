# Generated by Django 3.1.5 on 2025-05-28 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='joined_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(default='user', max_length=255),
            preserve_default=False,
        ),
    ]

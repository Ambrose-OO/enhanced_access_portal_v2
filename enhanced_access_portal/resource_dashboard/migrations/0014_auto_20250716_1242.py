# Generated by Django 3.1.5 on 2025-07-16 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0003_user_emailaddress'),
        ('resource_dashboard', '0013_auto_20250714_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='owner_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='login_page.user'),
        ),
    ]

# Generated by Django 3.1.5 on 2025-07-14 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource_dashboard', '0010_auto_20250710_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vms',
            name='project_id',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='resource_dashboard.projects'),
        ),
    ]

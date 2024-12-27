# Generated by Django 4.2.17 on 2024-12-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('global', 'Global User'), ('ecommerce', 'Ecommerce App User'), ('test', 'Test App User'), ('marketplace', 'Marketplace App User')], default='global', max_length=50),
        ),
    ]

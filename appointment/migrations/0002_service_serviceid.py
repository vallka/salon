# Generated by Django 4.1.7 on 2024-12-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='serviceid',
            field=models.BigIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]

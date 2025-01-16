# Generated by Django 4.1.7 on 2024-12-21 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('blocked', models.CharField(max_length=20)),
                ('block_reason', models.CharField(max_length=255)),
                ('appointments', models.IntegerField()),
                ('no_shows', models.IntegerField()),
                ('total_sales', models.DecimalField(decimal_places=2, max_digits=6)),
                ('outstanding', models.DecimalField(decimal_places=2, max_digits=6)),
                ('gender', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('accepts_marketing', models.CharField(max_length=20)),
                ('accepts_sms_marketing', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('suite', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('post_code', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('added', models.DateField(blank=True, null=True)),
                ('note', models.TextField()),
                ('referral_source', models.CharField(max_length=255)),
            ],
        ),
    ]

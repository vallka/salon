# Generated by Django 4.2.3 on 2023-07-06 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fresha', '0003_alter_category_description_alter_group_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.CharField(max_length=25, primary_key=True, serialize=False),
        ),
    ]

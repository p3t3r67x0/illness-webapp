# Generated by Django 3.0.4 on 2020-03-24 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0016_auto_20200324_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='zip_code_str',
        ),
    ]

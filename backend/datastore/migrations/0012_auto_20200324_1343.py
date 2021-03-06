# Generated by Django 3.0.4 on 2020-03-24 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datastore', '0011_auto_20200323_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='County')),
                ('longitude', models.FloatField(verbose_name='Long geo coord')),
                ('latitude', models.FloatField(verbose_name='Lat geo coord')),
            ],
        ),
        migrations.RenameField(
            model_name='report',
            old_name='zip_code',
            new_name='zip_code_str',
        ),
        migrations.CreateModel(
            name='ZIPCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.PositiveIntegerField(verbose_name='Zip code')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datastore.County')),
            ],
        ),
    ]

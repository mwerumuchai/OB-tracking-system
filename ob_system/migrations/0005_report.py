# Generated by Django 2.0 on 2018-01-18 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ob_system', '0004_crime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('id_no', models.IntegerField()),
                ('ref_no', models.CharField(blank=True, max_length=150)),
                ('case_file_no', models.CharField(blank=True, max_length=150)),
                ('crime_description', models.TextField()),
                ('time', models.TimeField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('crime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ob_system.Crime')),
            ],
        ),
    ]

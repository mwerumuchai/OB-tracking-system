# Generated by Django 2.0 on 2018-01-13 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crime_type', models.TextField(max_length=500)),
                ('crime_description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CriminalProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criminal_name', models.CharField(max_length=30)),
                ('birth_date', models.DateTimeField(null=True)),
                ('criminal_id', models.IntegerField()),
                ('criminal_image', models.ImageField(upload_to='criminalphotos/')),
                ('crime_committed', models.CharField(max_length=500)),
                ('location', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='OccurrenceBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ob_no', models.IntegerField()),
                ('ref_no', models.IntegerField(blank=True)),
                ('case_file_no', models.IntegerField(blank=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.CharField(max_length=250)),
                ('nature_of_occurence', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_no', models.IntegerField()),
                ('rank', models.TextField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporter_name', models.TextField(blank=True, max_length=150)),
                ('reporter_id', models.IntegerField(blank=True)),
                ('report_description', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='occurrencebook',
            name='badge_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ob_system.Officer'),
        ),
        migrations.AddField(
            model_name='occurrencebook',
            name='crime_committed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ob_system.CriminalProfile'),
        ),
        migrations.AddField(
            model_name='booking',
            name='badge_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ob_system.Officer'),
        ),
        migrations.AddField(
            model_name='booking',
            name='crime_committed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ob_system.OccurrenceBook'),
        ),
        migrations.AddField(
            model_name='booking',
            name='criminal_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ob_system.CriminalProfile'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

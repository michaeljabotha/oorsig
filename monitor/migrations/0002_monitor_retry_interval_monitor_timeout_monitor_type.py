# Generated by Django 4.0 on 2022-08-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='retry_interval',
            field=models.IntegerField(blank=True, default=30, verbose_name='Retry Interval'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='timeout',
            field=models.IntegerField(blank=True, default=10, verbose_name='Timeout'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='type',
            field=models.CharField(choices=[('http', 'Http(s)'), ('ping', 'Ping'), ('dns', 'DNS'), ('tcp', 'TCP')], default='http', max_length=255, verbose_name='Type'),
        ),
    ]

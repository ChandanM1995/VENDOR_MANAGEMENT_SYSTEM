# Generated by Django 4.2.7 on 2023-12-01 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='HistoricalPerformances', to='sellers.vendor'),
        ),
    ]

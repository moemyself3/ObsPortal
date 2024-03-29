# Generated by Django 4.0.5 on 2023-04-19 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_alter_device_devicetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='devicetype',
            field=models.CharField(choices=[('Camera', 'Camera'), ('CoverCalibrator', 'CoverCalibrator'), ('Dome', 'Dome'), ('FilterWheel', 'FilterWheel'), ('Focuser', 'Focuser'), ('ObservingConditions', 'ObservingConditions'), ('Rotator', 'Rotator'), ('SafteyMonitor', 'SafetyMonitor'), ('Site', 'Site'), ('Switch', 'Switch'), ('Telescope', 'Telescope')], max_length=20, null=True, verbose_name='Device Type'),
        ),
    ]

# Generated by Django 4.1 on 2022-12-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_timetable_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='End',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Start',
            field=models.CharField(max_length=100),
        ),
    ]

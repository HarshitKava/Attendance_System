# Generated by Django 4.1 on 2022-12-12 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_alter_timetable_end_alter_timetable_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject', models.CharField(default=' ', max_length=100, null=True)),
                ('Code', models.CharField(default=' ', max_length=100, null=True)),
                ('Batch', models.CharField(default=' ', max_length=100, null=True)),
                ('RoomNo', models.CharField(default=' ', max_length=100, null=True)),
                ('RollNo', models.CharField(default=' ', max_length=100, null=True)),
                ('ips', models.CharField(default=' ', max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Batch',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Code',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Day',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='End',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Faculty_id',
            field=models.CharField(default=' ', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='RoomNo',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Start',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='Subject',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-11 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0004_alter_timeslot_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.timeslot')),
            ],
        ),
    ]

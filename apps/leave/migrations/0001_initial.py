# Generated by Django 3.2.9 on 2021-11-18 04:18

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
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(0, 'Sick leave (Illness or Injury)'), (1, 'Personal/Casual'), (2, 'Bereavement leave (Immediate Family)'), (3, 'Bereavement leave (Other)'), (4, 'Jury duty or legal'), (5, 'Emergency'), (6, 'Unpaid'), (7, 'TC Granted'), (8, 'COVID'), (9, 'Replacement'), (10, 'Maternity'), (11, 'Paternity'), (12, 'Menstrual'), (13, 'Other')])),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Denied')], default=0)),
                ('num_of_days', models.FloatField(verbose_name='number of days')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('additional_information', models.TextField(blank=True, null=True)),
                ('denied_reason', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaveDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.IntegerField(choices=[(0, 'First half'), (1, 'Second half'), (2, 'Full')], default=2)),
                ('additional_information', models.TextField(null=True)),
                ('leave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_day', to='leave.leave')),
            ],
        ),
    ]

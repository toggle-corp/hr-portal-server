# Generated by Django 3.2.9 on 2021-11-11 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], help_text='Choose Gender', max_length=10, null=True),
        ),
    ]

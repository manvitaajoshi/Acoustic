# Generated by Django 3.1.3 on 2020-12-23 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acousticuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='acousticuser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='acousticuser',
            name='username',
        ),
    ]

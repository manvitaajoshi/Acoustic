# Generated by Django 3.1.3 on 2021-01-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0014_auto_20210115_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 2.2.5 on 2019-12-05 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191205_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='settings',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]

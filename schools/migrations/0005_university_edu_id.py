# Generated by Django 2.2.3 on 2019-07-22 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0004_auto_20190722_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='edu_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]

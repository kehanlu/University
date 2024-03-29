# Generated by Django 2.2.3 on 2019-07-24 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0007_auto_20190723_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='register_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='schools.University')),
            ],
        ),
    ]
